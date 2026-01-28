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
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

# import prompt
from .prompt import prompt_QA_rule_filter_v3, prompt_QA_rule_filter_v3_en, prompt_image_relevance_filter_v1, prompt_image_relevance_filter_v1_en
import tool.extract_rel
import tool.extract_ver


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

# os.environ["OPENAI_API_KEY"] = ""
# base_url=""

def call_model_old(messages, modelname):
    start = time.perf_counter()
    k = 3
    # ouput = ""
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
                    if response_json['error']['message'] == 'Invalid image data.':
                        ouput = 'Invalid'
                        return ouput, None
                print(f"response_json faild. {response_json=}")
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
    if_rule = line.get("IF_RULE", "")
    if if_rule != "" and if_rule != "error":
        write_to_file(line)
        return 1

    ques_final = line.get("QA_final", "")
    img_path = Config.img_dir + line["image_path"].split('/')[-1]
    system_prompt = ""

    if ques_final == "" or ques_final == "error" or ques_final == "reject":
        write_to_errorfile(line)
        return 1
    ques_final = ques_final.replace("```json", "").replace("```", "").replace("\n", "")
    try:
        qa_dict = json.loads(ques_final)
    except Exception as e:
        print(e)
        write_to_errorfile(line)
        return 1
    ### 基于rule的过滤
    img_type = img_path.split('.')[-1]
    if img_type == 'jpg':
        img_type = 'jpeg'
    # 将图片文件转换为 Base64 编码
    with open(img_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    img_input = f"data:image/{img_type};base64,{encoded_image}"
    mssg_rule = [{"role": "system", "content": system_prompt}]
    if line['data_language'] == "CN":
        prompt_format = prompt_QA_rule_filter_v3
    else:
        prompt_format = prompt_QA_rule_filter_v3_en
    prompt_rule = prompt_format.format(question = qa_dict["question"], answer = qa_dict["answer"])
    mssg_rule.append(
        {
            "role": "user", 
            "content": [
                {"type": "text", "text": prompt_rule},
                {"type": "image_url","image_url": {"url": img_input}}
            ]
        }
    )

    try:
        if_rule,_ = call_model(mssg_rule, Config.call_modelname)
        if if_rule == 'Invalid' or if_rule == 'reject':
            line['IF_RULE'] = if_rule
            write_to_errorfile(line)
            return 1
        if if_rule == "": raise
        line['IF_RULE'] = if_rule
        write_to_file(line)
        return 1

    except Exception as e:
        print(e)
        print('IF_RULE:', traceback.format_exc())
        # line['IF_RULE'] = "error"
        # write_to_errorfile(line)
        return 0

def image_filter_process_line(line):
    img_rel = line.get("Image_relevance", "")
    if img_rel != "" and img_rel != "error":
        write_to_file(line)
        return 1

    img_path = Config.img_dir + line["image_path"].split('/')[-1]
    img_label = line["pop_words"]
    img_cap = line.get("image_caption", "")
    system_prompt = ""

    if img_cap == "" or img_cap == "error" or img_cap == "reject":
        write_to_errorfile(line)
        return 1
    
    ### 图片标签相关性过滤
    img_type = img_path.split('.')[-1]
    if img_type == 'jpg':
        img_type = 'jpeg'
    # 将图片文件转换为 Base64 编码
    with open(img_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    img_input = f"data:image/{img_type};base64,{encoded_image}"
    mssg_imgrel = [{"role": "system", "content": system_prompt}]
    if line['data_language'] == "CN":
        prompt_format = prompt_image_relevance_filter_v1
    else:
        prompt_format = prompt_image_relevance_filter_v1_en
    prompt_imgrel = prompt_format.format(caption = img_cap, label = img_label)
    mssg_imgrel.append(
        {
            "role": "user", 
            "content": [
                {"type": "text", "text": prompt_imgrel},
                {"type": "image_url","image_url": {"url": img_input}}
            ]
        }
    )

    try:
        img_rel,_ = call_model(mssg_imgrel, Config.call_modelname)
        if img_rel == 'Invalid' or img_rel == 'reject':
            line['Image_relevance'] = img_rel
            write_to_errorfile(line)
            return 1
        if img_rel == "": raise
        line['Image_relevance'] = img_rel
        write_to_file(line)
        return 1

    except Exception as e:
        print(e)
        print('Image_relevance:', traceback.format_exc())
        # line['Image_relevance'] = "error"
        # write_to_errorfile(line)
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

def API_Filter(args):

    # 初始化 OpenAI 客户端
    client = OpenAI(
        # 请根据实际情况修改，如使用环境变量等配置
        api_key="aib_Ovis_model_47156f",
        base_url="https://offline-openai-keys.alibaba-inc.com/v1",
    )

    # ==============================
    Config.call_modelname = args.model_name
    print(f"Model Name: {Config.call_modelname}")
    concurrent_num = args.Con_num
    data_key = args.dataset_key
    folder = f"/mnt/workspace/cv_multimodal/zgd/Project/worldknowledge/QA_generate/results/{data_key}"
    if not os.path.exists(folder):
        os.makedirs(folder)

    # ==============================

    start_time = time.perf_counter()
    local_time = time.localtime()
    if_rule_filter = args.IF_RULE
    if_imgrel_filter = args.IF_RELEVANCE

    # ==============================
    if if_rule_filter:
        start_time = time.perf_counter()
        local_time = time.localtime()
        folder_1 = f"/mnt/workspace/cv_multimodal/zgd/Project/worldknowledge/QA_generate/results/{data_key}/rule_res"
        if not os.path.exists(folder_1):
            os.makedirs(folder_1)
        origin_file = f"{folder}/final_res/{data_key}_gen_final.jsonl"
        Config.new_file = f"{folder}/rule_res/{data_key}_gen_rule.jsonl"
        Config.error_file = f"{folder}/rule_res/{data_key}_gen_rule_error.jsonl"
        with open(origin_file, "r", encoding='utf-8', buffering=8192) as fin:
            data_new = [json.loads(line) for line in fin if line.strip()]
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
                return
                # old_file = Config.new_file.split(".")[0] + f'_{local_time.tm_mon}-{local_time.tm_mday}-{local_time.tm_hour}-{local_time.tm_min}.jsonl'
                # write_jsonl(data_exsists, old_file)
                # data_new = data_exsists
                # fin =  open(Config.new_file, "w", encoding='utf-8')
        else:
            fin =  open(Config.new_file, "w", encoding='utf-8')

        l = len(data_new)

        with Pool(processes=concurrent_num) as pool:
            sleep_time = random.uniform(0, 1)
            sleep(sleep_time)
            results = list(tqdm(pool.imap(process_line, data_new), total=len(data_new)))       
            correct = np.sum(np.array(results))
            print("总数：", l) 
            print("成功数：", correct) 
            print("错误数：", l - correct)
        
        tool.extract_ver.extract(Config.new_file)
        end_time = time.perf_counter()
        execution_time_ms = (end_time - start_time) / 60
        print(f"首次执行耗时: {execution_time_ms} mins")


    if if_imgrel_filter:
        start_time = time.perf_counter()
        local_time = time.localtime()
        folder_1 = f"/mnt/workspace/cv_multimodal/zgd/Project/worldknowledge/QA_generate/results/{data_key}/imgrel_res"
        if not os.path.exists(folder_1):
            os.makedirs(folder_1)
        origin_file = f"{folder}/cap_res/{data_key}_gen_cap.jsonl"
        Config.new_file = f"{folder}/imgrel_res/{data_key}_gen_imgrel.jsonl"
        Config.error_file = f"{folder}/imgrel_res/{data_key}_gen_imgrel_error.jsonl"
        with open(origin_file, "r", encoding='utf-8', buffering=8192) as fin:
            data_new = [json.loads(line) for line in fin if line.strip()]
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
                return
                # old_file = Config.new_file.split(".")[0] + f'_{local_time.tm_mon}-{local_time.tm_mday}-{local_time.tm_hour}-{local_time.tm_min}.jsonl'
                # write_jsonl(data_exsists, old_file)
                # data_new = data_exsists
                # fin =  open(Config.new_file, "w", encoding='utf-8')
        else:
            fin =  open(Config.new_file, "w", encoding='utf-8')

        l = len(data_new)

        with Pool(processes=concurrent_num) as pool:
            sleep_time = random.uniform(0, 1)
            sleep(sleep_time)
            results = list(tqdm(pool.imap(image_filter_process_line, data_new), total=len(data_new)))       
            correct = np.sum(np.array(results))
            print("总数：", l) 
            print("成功数：", correct) 
            print("错误数：", l - correct)
        
        tool.extract_rel.extract(Config.new_file)
        end_time = time.perf_counter()
        execution_time_ms = (end_time - start_time) / 60
        print(f"首次执行耗时: {execution_time_ms} mins")
