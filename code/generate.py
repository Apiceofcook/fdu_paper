import requests
import json
import orjson
import traceback
import re
import sys
from time import sleep
from tqdm.asyncio import tqdm
from multiprocessing import Pool
import numpy as np  
from openai import OpenAI
import pandas as pd
import os
import base64
import random

import shutil
from io import StringIO
import oss2 as oss
import io
from io import BytesIO
from datetime import datetime
import time
import tarfile
import argparse
from PIL import Image
from PIL import ImageFile
import tempfile
import subprocess
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

# import prompt
from .prompt import prompt_cap_v3, prompt_cap_v3_en, \
    prompt_rec_QA_wimg_v4, prompt_rec_QA_wimg_v4_en, \
    prompt_rec_QA_woimg_v1, \
    prompt_know_QA_v3, prompt_know_QA_v3_en, \
    prompt_final_QA_v3, prompt_final_QA_v3_en, \
    prompt_know_QA_list_v1, prompt_know_QA_list_v1_en, \
    prompt_final_QA_cot_v1, prompt_final_QA_cot_v1_en

model_list = {
    'bu': ['gpt-4o-mini', 'gpt-4o'],
    'idea': ["gpt-4o-mini-0718", "gpt-4o-0513", "gemini-1.5-pro"]
}
request_url = {
    'bu': "https://offline-openai-keys.alibaba-inc.com/v1/chat/completions",
}
ak_key = {
    'bu': "aib_Ovis_model_47abc5",  # aib_ovis_7c56b5   aib_Ovis_model_ae5083  aib_Ovis_model_47abc5
}

class Config:
    call_modelname = ""
    new_file = ""
    error_file = ""
    # 初始化 OpenAI 客户端
    client = OpenAI(
        # 请根据实际情况修改，如使用环境变量等配置
        api_key="aib_Ovis_model_47156f",
        base_url="https://offline-openai-keys.alibaba-inc.com/v1",
    )
    img_dir = "/mnt/workspace/cv_multimodal/zgd/Data/wk_badcase/image/img/"


def call_model_old(messages, modelname):
    start = time.perf_counter()
    k = 3
    ouput = ""
    api_source = 'bu'
    input_json = {
        "model": modelname,
        "messages": messages,
        # "n": return_n,
        "temperature": 1.0
    }
    while(k > 0):
        k -= 1
        try:
            response = requests.post(
                request_url[api_source],
                json=input_json,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {ak_key[api_source]}"
                }
            )
            response_json = json.loads(response.text)
            if not response_json or 'error' in response_json:
                if 'error' in response_json:
                    if response_json['error']['message'] == 'Invalid image data.':
                        ouput = 'Invalid'
                        return ouput, None
                    # key limit检查    
                    if response_json['error']['message'] == 'reach proxy key limit':
                        limit_k = 0
                        while True:
                            print("reach proxy key limit...")
                            if limit_k >= 10:
                                break
                            elif limit_k >= 5:
                                time.sleep(600)
                            time.sleep(60)
                            # 重新执行API调用
                            response = requests.post(
                                request_url[api_source],
                                json=input_json,
                                headers={
                                    "Content-Type": "application/json",
                                    "Authorization": f"Bearer {ak_key[api_source]}"
                                }
                            )
                            response_json = json.loads(response.text)
                            
                            #检查是否还存在限制问题
                            if response_json and 'error' not in response_json:
                                result = []
                                for choice in response_json["choices"]:
                                    result.append(choice['message']['content'])
                                ouput = result[0]
                                if if_reject(ouput):
                                    ouput = ""
                                    break
                                return ouput, None
                            elif response_json['error']['message'] != 'reach proxy key limit':
                                print("continue")
                                break
                            limit_k += 1
                print(f"response_json faild. {response_json}")
                raise
            else:
                result = []
                for choice in response_json["choices"]:
                    result.append(choice['message']['content'])
                ouput = result[0]
                if if_reject(ouput):
                    # print("reject: ", ouput)
                    if k == 0:
                        ouput = "reject"
                    else:
                        ouput = ""
                        raise
                # print(ouput)

            if ouput != None and ouput != "":
                break
        except Exception as e:
            print(e)
            continue
    end = time.perf_counter()
    # print("API call time used: %.2f s" % (end-start))

    return ouput, None


def call_model(messages, modelname):
    start = time.perf_counter()
    k = 3
    while(k > 0):
        k -= 1
        reasoning_content = ""  # 用于收集完整思考过程
        answer_content = ""     # 用于收集完整回复内容
        is_answering = False    # 标记是否已经进入回复阶段
        try:
            completion = Config.client.chat.completions.create(
                model=modelname,
                messages=messages,
                extra_body={"enable_thinking": False},
                temperature=1.0,
                top_p=0.9,
                stream=True,
            )
        except Exception as e:
            print(e)
            if "reach proxy key limit" in str(e):
                limit_k = 0
                while True:
                    print("reach proxy key limit...")
                    if limit_k >= 10:
                        break
                    elif limit_k >= 5:
                        time.sleep(600)
                    time.sleep(60)
                    # 重新执行API调用
                    try:
                        completion = Config.client.chat.completions.create(
                            model=modelname,
                            reasoning_effort="low",
                            messages=messages,
                            extra_body={"enable_thinking": False},
                            temperature=1.0,
                            top_p=0.9,
                            stream=True,
                        )
                    except Exception as e:
                        if "reach proxy key limit" not in str(e):
                            break
                        else:
                            limit_k += 1
                            continue
                    for chunk in completion:
                        if not chunk.choices:
                            continue
                    
                        delta = chunk.choices[0].delta
                        if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
                            reasoning_content += delta.reasoning_content
                        if hasattr(delta, "content") and delta.content:
                            if not is_answering:
                                is_answering = True
                            answer_content += delta.content
                    if if_reject(answer_content):
                        # print("reject: ", ouput)
                        answer_content = "reject"
                        break
                    else:
                        return answer_content, None
            continue
        # print(completion)
        for chunk in completion:
            if not chunk.choices:
                continue
        
            delta = chunk.choices[0].delta
            if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
                reasoning_content += delta.reasoning_content
            if hasattr(delta, "content") and delta.content:
                if not is_answering:
                    is_answering = True
                answer_content += delta.content

        if if_reject(answer_content):
            # print("reject: ", ouput)
            if k == 0:
                answer_content = "reject"
            else:
                answer_content = ""
                continue
        
        if answer_content != None and answer_content != "":
            break
    
    end = time.perf_counter()
    return answer_content, None


def if_reject(text):
    lower_text = text.lower()
    # en = "i'm sorry" in lower_text and "i can't" in lower_text
    en = "i'm sorry" in lower_text
    en2 = "i'm very sorry" in lower_text
    # cn = "抱歉" in text and "无法" in text
    cn = "抱歉" in text
    return en or cn or en2


def write_to_file(info):
    if not isinstance(info, str):
        info = json.dumps(info, ensure_ascii=False)
    with open(Config.new_file, 'a', encoding='utf-8') as fin:
        fin.write(info + '\n')

def write_to_errorfile(info):
    if not isinstance(info, str):
        info = json.dumps(info, ensure_ascii=False)
    with open(Config.error_file, 'a', encoding='utf-8') as fin:
        fin.write(info + '\n')


def process_line(line):
    img_cap = line.get("image_caption", "")
    if img_cap != ""  and img_cap != "error":
        write_to_file(line)
        return 1

    topic = line["topic"]
    subtopics = line["subtopics"]
    lab_class = f"{topic}-{subtopics}"
    img_label = line["pop_words"]
    img_path = Config.img_dir + line["image_path"].split('/')[-1]
    system_prompt = ""

    ### caption生成
    if img_cap == "" or img_cap == "error":
        img_type = img_path.split('.')[-1]
        if img_type == 'jpg':
            img_type = 'jpeg'
        # 将图片文件转换为 Base64 编码
        try:
            with open(img_path, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(e)
            line['image_caption'] = 'Permission denied'
            write_to_errorfile(line)
            return 1
        img_input = f"data:image/{img_type};base64,{encoded_image}"
        mssg_cap = [{"role": "system", "content": system_prompt}]
        prompt_format = random.choice([prompt_cap_v3, prompt_cap_v3_en])
        if prompt_format == prompt_cap_v3:
            line['data_language'] = "CN"
        else:
            line['data_language'] = "EN"
        prompt_cap = prompt_format.format(label = img_label)
        mssg_cap.append(
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": prompt_cap},
                    {"type": "image_url","image_url": {"url": img_input}}
                ]
            }
        )

        try:
            img_cap,_ = call_model(mssg_cap, Config.call_modelname)
            if img_cap == 'Invalid' or img_cap == 'reject':
                line['image_caption'] = img_cap
                write_to_errorfile(line)
                return 1
            if img_cap == "": raise
            line['image_caption'] = img_cap
            write_to_file(line)
            return 1

        except Exception as e:
            print(e)
            print('image_caption:', traceback.format_exc())
            # line['image_caption'] = "error"
            # write_to_file(line)
            return 0

def process_line_rec(line):
    img_cap = line.get("image_caption", "")
    if img_cap == "" or img_cap == "error":
        # write_to_file(line)
        return 0
    
    ques_rec = line.get("QA_rec", "")
    if ques_rec != "" and ques_rec != "error":
        write_to_file(line)
        return 1

    topic = line["topic"]
    subtopics = line["subtopics"]
    lab_class = f"{topic}-{subtopics}"
    img_label = line["pop_words"]
    img_path = img_path = Config.img_dir + line["image_path"].split('/')[-1]
    system_prompt = ""

    ### question_rec生成
    mssg_rec = [{"role": "system", "content": system_prompt}]

    img_type = img_path.split('.')[-1]
    if img_type == 'jpg':
        img_type = 'jpeg'
    # 将图片文件转换为 Base64 编码
    with open(img_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    img_input = f"data:image/{img_type};base64,{encoded_image}"
    if line['data_language'] == "CN":
        prompt_format = prompt_rec_QA_wimg_v4
    else:
        prompt_format = prompt_rec_QA_wimg_v4_en
    prompt_rec = prompt_format.format(label = img_label, label_class = lab_class)
    mssg_rec.append(
    {
        "role": "user", 
        "content": [
            {"type": "text", "text": prompt_rec},
            {"type": "image_url","image_url": {"url": img_input}}
        ]
    }
    )
    
    try:
        ques_rec, _ = call_model(mssg_rec, Config.call_modelname)
        if ques_rec == 'Invalid' or ques_rec == 'reject':
            line['QA_rec'] = ques_rec
            write_to_errorfile(line)
            return 1
        if ques_rec == "": raise
        line['QA_rec'] = ques_rec
        write_to_file(line)
        return 1
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        # line['QA_rec'] = "error"
        # write_to_file(line)
        return 0

def process_final_line(line):
    qa_know = line.get("QA_know", "")
    qa_final = line.get("QA_final", "")
    if qa_know != "" and qa_final != "" and qa_know != "error" and qa_final != "error":
        write_to_file(line)
        return 1

    topic = line["topic"]
    subtopics = line["subtopics"]
    lab_class = f"{topic}-{subtopics}"
    img_label = line["pop_words"]
    img_cap = line["image_caption"]
    # ques_rec = line["QA_rec"]
    ques_rec = line.get("QA_rec", "")
    system_prompt = ""

    if ques_rec == "error" or ques_rec == "" or ques_rec == None:
        Invalid_num += 1
        write_to_errorfile(line)
        return 1

    ques_rec = ques_rec.replace("```json", "").replace("```", "").replace("\n", "")
    qa_know = line.get("QA_know", "")
    if qa_know == "" or qa_know == "error":
        if line['data_language'] == "CN":
            prompt_format = prompt_know_QA_v3
        else:
            prompt_format = prompt_know_QA_v3_en
        mssg_know = [{"role": "system", "content": system_prompt}]
        # print("prompt_format:\n", prompt_format)
        prompt_know = prompt_format.format(QA_rec = ques_rec, label = img_label, label_class = lab_class, caption = img_cap)
        mssg_know.append({"role": "user", "content": prompt_know})
        try:
            qa_know,_ = call_model(mssg_know, Config.call_modelname)
            if qa_know == 'Invalid' or qa_know == 'reject':
                line['QA_know'] = qa_know
                write_to_errorfile(line)
                return 1
            if qa_know == "": raise
            line['QA_know'] = qa_know

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            line['QA_know'] = "error"
            # write_to_file(line)
            return 0
    
    qa_final = line.get("QA_final", "")
    if qa_final == "" or qa_final == "error":
        mssg_final = [{"role": "system", "content": system_prompt}]
        qa_know = line['QA_know']
        if qa_know == "" or qa_know == "error":
            return 0
        qa_know = qa_know.replace("```json", "").replace("```", "").replace("\n", "")
        if line['data_language'] == "CN":
            prompt_format = prompt_final_QA_v3
        else:
            prompt_format = prompt_final_QA_v3_en
        prompt_final = prompt_format.format(label = img_label, QA_rec = ques_rec, QA_know = qa_know)
        mssg_final.append({"role": "user", "content": prompt_final})
        try:
            qa_final, _ = call_model(mssg_final, Config.call_modelname)
            if qa_final == 'Invalid' or qa_final == 'reject':
                line['QA_final'] = qa_final
                write_to_errorfile(line)
                return 1
            if qa_final == "": raise
            line['QA_final'] = qa_final
            write_to_file(line)
            return 1
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            # line['QA_final'] = "error"
            # write_to_file(line)
            return 0

def process_final_list_line(line): 
    qa_know_text = line.get("QA_know_list_text", "")
    qa_final_list = line.get("QA_final_list", "")
    if qa_know_text != "" and qa_final_list != [] and qa_know_text != "error" and qa_final_list != "":
        write_to_file(line)
        return 1

    topic = line["topic"]
    subtopics = line["subtopics"]
    lab_class = f"{topic}-{subtopics}"
    img_label = line["pop_words"]
    img_cap = line["image_caption"]
    # ques_rec = line["QA_rec"]
    ques_rec = line.get("QA_rec", "")
    system_prompt = ""

    if ques_rec == "error" or ques_rec == "" or ques_rec == None:
        Invalid_num += 1
        write_to_errorfile(line)
        return 1

    ques_rec = ques_rec.replace("```json", "").replace("```", "").replace("\n", "")
    qa_know_text = line.get("QA_know_list_text", "")
    if qa_know_text == "" or qa_know_text == "error":
        if line['data_language'] == "CN":
            prompt_format = prompt_know_QA_list_v1
        else:
            prompt_format = prompt_know_QA_list_v1_en
        mssg_know = [{"role": "system", "content": system_prompt}]
        # print("prompt_format:\n", prompt_format)
        prompt_know = prompt_format.format(QA_rec = ques_rec, label = img_label, label_class = lab_class, caption = img_cap)
        # print(prompt_know)
        mssg_know.append({"role": "user", "content": prompt_know})
        try:
            qa_know_text,_ = call_model(mssg_know, Config.call_modelname)
            # print(qa_know_text)
            if qa_know_text == 'Invalid' or qa_know_text == 'reject':
                line['QA_know_list_text'] = qa_know_text
                write_to_errorfile(line)
                return 0
            if qa_know_text == "": raise
            line['QA_know_list_text'] = qa_know_text
            # write_to_file(line)
            # return 1

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            line['QA_know_list_text'] = "error"
            # write_to_file(line)
            return 0
    
    qa_know_list = qa_know_text.replace("```json", "").replace("```", "").replace("\n", "")
    try:
        qa_know_list = json.loads(qa_know_list)
        line['QA_know_list'] = qa_know_list
        # return 1
    except Exception as e:
        write_to_errorfile(line)
        print(e)
        return 0
    
    # qa_know_n = 0
    # if qa_final_list == "" or qa_final_list == []:
    qa_final_list = []
    for qa_know in qa_know_list:
        # qa_final = line.get("QA_final", "")
        # qa_final_list = []
        mssg_final = [{"role": "system", "content": system_prompt}]
        # qa_know = line['QA_know']
        # if qa_know == "" or qa_know == "error":
        #     return 0
        if not isinstance(qa_know, dict):
            return 0
        if "question" not in qa_know.keys() or "answer" not in qa_know.keys():
            return 0
        # qa_know = qa_know.replace("```json", "").replace("```", "").replace("\n", "")
        if line['data_language'] == "CN":
            prompt_format = prompt_final_QA_cot_v1
        else:
            prompt_format = prompt_final_QA_cot_v1_en
        prompt_final = prompt_format.format(label = img_label, QA_rec = ques_rec, QA_know = qa_know)
        mssg_final.append({"role": "user", "content": prompt_final})
        try:
            qa_final, _ = call_model(mssg_final, Config.call_modelname)
            if qa_final == 'Invalid' or qa_final == 'reject':
                # line['QA_final'] = qa_final
                # write_to_errorfile(line)
                # return 0
                continue
            if qa_final == "": continue
            qa_final = qa_final.replace("```json", "").replace("```", "").replace("\n", "")
            # print("----------------------qa_final--------------------\n", qa_final)
            qa_final = json.loads(qa_final)
            # line['QA_final'] = qa_final
            qa_final_list.append(qa_final)
            # write_to_file(line)
            # return 1
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            # line['QA_final'] = "error"
            # write_to_file(line)
            # return 0
            continue
    if qa_final_list != []:
        line['QA_final_list'] = qa_final_list
        write_to_file(line)
        return 1
    else:
        write_to_errorfile(line)
        return 0

def return_gen_list(origin_list, new_list):
    """
    使用pandas处理大数据量的情况
    """
    # 转换为DataFrame
    origin_df = pd.DataFrame(origin_list)
    new_df = pd.DataFrame(new_list)
    
    # 找出origin中有而new中没有的id
    if not new_df.empty:
        mask = ~origin_df['id'].isin(new_df['id'])
        result_df = origin_df[mask]
    else:
        result_df = origin_df
    
    # 转回字典列表
    return result_df.to_dict('records')

def write_jsonl(dict_list, filename: str, chunk_size: int = 10000, buffer_size: int = 65536) -> None:
    # 预估文件大小并预分配
    total_items = len(dict_list)
    with open(filename, 'wb', buffering=buffer_size) as f:
        # 分块处理，避免内存溢出
        for i in range(0, total_items, chunk_size):
            chunk = dict_list[i:i + chunk_size]# 批量序列化这个块
            serialized_chunk = []
            for item in chunk:
                serialized_chunk.append(orjson.dumps(item))
            #一次性写入这个块
            content = b'\n'.join(serialized_chunk)
            if i > 0:
                # 不是第一块时添加换行
                f.write(b'\n')
            f.write(content)
        
        f.write(b'\n')# 文件末尾换行
    # print(f"极致优化写入完成: {total_items}条记录")

def API_GEN(args):
    # ==============================
    # call_modelname = 'gpt-4o-0806'
    # call_modelname = 'gpt-4o'
    Config.call_modelname = args.model_name
    print(f"Model Name: {Config.call_modelname}")
    concurrent_num = args.Con_num
    data_key = args.dataset_key
    folder = f"/mnt/workspace/cv_multimodal/zgd/Project/worldknowledge/QA_generate/results/{data_key}"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # ==============================

    # start_time = time.perf_counter()
    # local_time = time.localtime()
    if_cap = args.IF_CAP
    if_rec = args.IF_REC
    if_merge = args.IF_MERGE
    # if_retry = args.dataset_key

    # ==============================
    if if_cap:
        if_skip = 0
        start_time = time.perf_counter()
        local_time = time.localtime()
        folder_1 = f"/mnt/workspace/cv_multimodal/zgd/Project/worldknowledge/QA_generate/results/{data_key}/cap_res"
        if not os.path.exists(folder_1):
            os.makedirs(folder_1)
        origin_file = args.origin_file
        Config.new_file = f"{folder}/cap_res/{data_key}_gen_cap.jsonl"
        Config.error_file = f"{folder}/cap_res/{data_key}_gen_cap_error.jsonl"
        with open(origin_file, 'r', encoding='utf-8') as f:
            data_new = json.load(f)
        if os.path.exists(Config.error_file):
            with open(Config.error_file, "r", encoding='utf-8', buffering=8192) as fin:
                data_error = [json.loads(line) for line in fin if line.strip()]
            data_new = return_gen_list(data_new, data_error)
        if os.path.exists(Config.new_file):
            with open(Config.new_file, "r", encoding='utf-8', buffering=8192) as fin:
                data_exsists = [json.loads(line) for line in fin if line.strip()]
            if len(data_exsists) != len(data_new):
                data_new = return_gen_list(data_new, data_exsists)
            else:
                print("Alreaady Success!")
                if_skip = 1
                # old_file = Config.new_file.split(".")[0] + f'_{local_time.tm_mon}-{local_time.tm_mday}-{local_time.tm_hour}-{local_time.tm_min}.jsonl'
                # write_jsonl(data_exsists, old_file)
                # data_new = data_exsists
                # fin =  open(Config.new_file, "w", encoding='utf-8')
        else:
            fin =  open(Config.new_file, "w", encoding='utf-8')

        l = len(data_new)
        if not if_skip:
            with Pool(processes=concurrent_num) as pool:
                sleep_time = random.uniform(0, 1)
                sleep(sleep_time)
                results = list(tqdm(pool.imap(process_line, data_new), total=len(data_new)))       
                correct = np.sum(np.array(results))
                print("总数：", l) 
                print("成功数：", correct) 
                print("错误数：", l - correct)
            
            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) / 60
            print(f"首次执行耗时: {execution_time_ms} mins")

    # ==============================
    if if_rec:
        if_skip = 0
        start_time = time.perf_counter()
        local_time = time.localtime()
        folder_1 = f"/mnt/workspace/cv_multimodal/zgd/Project/worldknowledge/QA_generate/results/{data_key}/rec_res"
        if not os.path.exists(folder_1):
            os.makedirs(folder_1)
        origin_file = f"{folder}/imgrel_res/{data_key}_gen_imgrel_m3.jsonl"
        Config.new_file = f"{folder}/rec_res/{data_key}_gen_rec.jsonl"
        Config.error_file = f"{folder}/rec_res/{data_key}_gen_rec_error.jsonl"
        # with open(origin_file, 'r', encoding='utf-8') as f:
        #     data_new = json.load(f)
        with open(origin_file, "r", encoding='utf-8', buffering=8192) as fin:
            data_new = [json.loads(line) for line in fin if line.strip()]
        if os.path.exists(Config.error_file):
            data_error = []
            with open(Config.error_file, "r", encoding='utf-8') as fin:
                lines = fin.readlines()
                for line in lines:
                    data = json.loads(line)
                    data_error.append(data)
            data_new = return_gen_list(data_new, data_error)
        if os.path.exists(Config.new_file):
            with open(Config.new_file, "r", encoding='utf-8', buffering=8192) as fin:
                data_exsists = [json.loads(line) for line in fin if line.strip()]
            if len(data_exsists) != len(data_new):
                data_new = return_gen_list(data_new, data_exsists)
            else:
                print("Alreaady Success!")
                if_skip = 1
                # old_file = Config.new_file.split(".")[0] + f'_{local_time.tm_mon}-{local_time.tm_mday}-{local_time.tm_hour}-{local_time.tm_min}.jsonl'
                # write_jsonl(data_exsists, old_file)
                # data_new = data_exsists
                # fin =  open(Config.new_file, "w", encoding='utf-8')
        else:
            fin =  open(Config.new_file, "w", encoding='utf-8')

        l = len(data_new)
        if not if_skip:
            with Pool(processes=concurrent_num) as pool:
                sleep_time = random.uniform(0, 1)
                sleep(sleep_time)
                results = list(tqdm(pool.imap(process_line_rec, data_new), total=len(data_new)))       
                correct = np.sum(np.array(results))
                print("总数：", l) 
                print("成功数：", correct) 
                print("错误数：", l - correct)
            
            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) / 60
            print(f"首次执行耗时: {execution_time_ms} mins")

    # ==============================
    if if_merge:
        if_skip = 0
        start_time = time.perf_counter()
        local_time = time.localtime()
        folder_1 = f"/mnt/workspace/cv_multimodal/zgd/Project/worldknowledge/QA_generate/results/{data_key}/final_res"
        if not os.path.exists(folder_1):
            os.makedirs(folder_1)
        origin_file = f"{folder}/rec_res/{data_key}_gen_rec.jsonl"
        Config.new_file = f"{folder}/final_res/{data_key}_gen_final.jsonl"
        Config.error_file = f"{folder}/final_res/{data_key}_gen_fianl_error.jsonl"
        with open(origin_file, "r", encoding='utf-8', buffering=8192) as fin:
            data_final = [json.loads(line) for line in fin if line.strip()]
        if os.path.exists(Config.error_file):
            # data_error = []
            # with open(Config.error_file, "r", encoding='utf-8') as fin:
            #     lines = fin.readlines()
            #     for line in lines:
            #         data = json.loads(line)
            #         data_error.append(data)
            with open(Config.error_file, "r", encoding='utf-8', buffering=8192) as fin:
                data_error = [json.loads(line) for line in fin if line.strip()]
            data_final = return_gen_list(data_final, data_error)
        if os.path.exists(Config.new_file):
            with open(Config.new_file, "r", encoding='utf-8', buffering=8192) as fin:
                data_exsists = [json.loads(line) for line in fin if line.strip()]
            if len(data_exsists) != len(data_final):
                data_final = return_gen_list(data_final, data_exsists)
            else:
                print("Alreaady Success!")
                if_skip = 1
                # old_file = Config.new_file.split(".")[0] + f'_{local_time.tm_mon}-{local_time.tm_mday}-{local_time.tm_hour}-{local_time.tm_min}.jsonl'
                # write_jsonl(data_exsists, old_file)
                # data_final = data_exsists
                # fin =  open(Config.new_file, "w", encoding='utf-8')
        else:
            fin =  open(Config.new_file, "w", encoding='utf-8')

        l = len(data_final)
        print(l)

        if not if_skip:
            with Pool(processes=concurrent_num) as pool:
                sleep_time = random.uniform(0, 1)
                sleep(sleep_time)
                results = list(tqdm(pool.imap(process_final_list_line, data_final), total=len(data_final)))       
                correct = np.sum(np.array(results))
                print("总数：", l) 
                print("成功数：", correct) 
                print("错误数：", l - correct)

            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) / 60
            print(f"首次合并执行耗时: {execution_time_ms} mins")
        