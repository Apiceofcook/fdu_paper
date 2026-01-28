prompt_cap_v1 = """
            该图片与{label}相关，请先结合{label}相关的知识仔细描述图片中的内容，然后补充{label}相关的知识
            """.strip()

prompt_cap_v2 = """
            该图片与{label}相关，请仔细描述图片中的内容，然后结合图片内容补充{label}相关的知识
            """.strip()

prompt_cap_v3 = """
            该图片与{label}相关，请描述图片中的内容，并结合{label}相关的知识进行补充，最后介绍{label}相关的知识，主要介绍相关且重要的内容，要求1000字以内
            """.strip()

prompt_cap_v2_en = """
            This image is related to {label}. Please carefully describe the content in the image, and then supplement knowledge related to {label} based on the image content.
            """.strip()

prompt_cap_v3_en = """
            This image is related to {label}. Please describe the content in the image and supplement it with knowledge related to {label}. Finally, introduce knowledge about {label}, mainly focusing on relevant and important content, Required within 800 words.
            """.strip()

prompt_cap_v3 = """
            该图片与{label}相关，请仔细描述图片中的内容，然后结合图片内容补充{label}相关的知识。
            如果你十分肯定图片与{label}不相关，请只返回【不相关】。
            如果你并不知道{label}相关的知识，则只用仔细描述图片中的内容即可。
            """.strip()

prompt_rec_QA_wimg_v1 = """
            现在我给你提供一张图片和与该图片相关的知识，还有生成的问题需要相关的类别,请根据图片生成一个关联图片问题和对应的标准答案。生成的问题是根据图片可以提出的问题,而且这个问题的答案必须严格同时既是图片中出现的实体,也是相关的文档、补充知识出现过的实体，此外生成的问题需与类别相关
            生成的问题必须满足以下要求:
             
            1. 生成的问题必须可以用图片中出现的实体作为答案,是不需要关联任何图片中实体以外的知识就可以回答的。例如,不要提问“图片中展现的运河位于哪个国家?”,因为这个问题的答案不是一个实体,而且答案也并不会出现在图片中。也避免提问“图片中的这张海报是谁设计的?”因为这个问题需要图片之外的知识,从图片中看不出来。也不要问“图片中的晶体主要成分是什么?”,因为这个问题的答案从图片中也看不出来。也尽量不要询问“图片中的景色拍摄于哪个地区?”,这个问题从图片中也很难看出来。
            2. 所提出的问题必须有且只有一个明确且无争议的实体作为答案,且问题表述中不应存在任何形式的模糊性或歧义。例如,避免提问“图片中的是什么?”因为无法确定具体指的是什么东西,图片中可能有多个实体。
            3. 避免同时询问两个问题,所提出的问题应该有且仅有一个具体的问题,不能够被拆分成两个问题,比如"图片中左上角和下方分别是什么东西?"不合适,因为这个问题相当于是同时问了两个问题,也会有两个答案。
            4. 如果问题的答案为英文,请给出中文翻译后的答案和括号里带上英文原名,格式如:雅各布·福格(Jakob Fugger)。
            5. 请用简体中文返回结果,不要繁体中文。
            6. 生成的问题需要与给定的类别相关
            请按照下面的格式返回生成的问题和答案: {{"question": "此处为生成问题", "answer": "此处为答案"}}
            ### 让我们开始吧!
            类别：{question_class}
            相关知识：{knowledge}
            """.strip()

prompt_rec_QA_wimg_v2 = """
            现在我给你提供一张图片和与该图片相关的标签，还有生成的问题需要相关的类别,请根据图片生成一个关联图片问题和对应的标准答案。生成的问题是根据图片可以提出的问题,而且这个问题的答案必须严格是同时既是图片中出现的实体,而且是与给出的标签相关的，此外生成的问题需与类别相关
            生成的问题必须满足以下要求:
             
            1. 生成的问题必须可以用图片中出现的实体作为答案,是不需要关联任何图片中实体以外的知识就可以回答的。例如,不要提问“图片中展现的运河位于哪个国家?”,因为这个问题的答案不是一个实体,而且答案也并不会出现在图片中。也避免提问“图片中的这张海报是谁设计的?”因为这个问题需要图片之外的知识,从图片中看不出来。也不要问“图片中的晶体主要成分是什么?”,因为这个问题的答案从图片中也看不出来。也尽量不要询问“图片中的景色拍摄于哪个地区?”,这个问题从图片中也很难看出来。
            2. 所提出的问题必须有且只有一个明确且无争议的实体作为答案,且问题表述中不应存在任何形式的模糊性或歧义。例如,避免提问“图片中的是什么?”因为无法确定具体指的是什么东西,图片中可能有多个实体。
            3. 避免同时询问两个问题,所提出的问题应该有且仅有一个具体的问题,不能够被拆分成两个问题,比如"图片中左上角和下方分别是什么东西?"不合适,因为这个问题相当于是同时问了两个问题,也会有两个答案。
            4. 如果问题的答案为英文,请给出中文翻译后的答案和括号里带上英文原名,格式如:雅各布·福格(Jakob Fugger)。
            5. 请用简体中文返回结果,不要繁体中文。
            6. 生成的问题需要与给定的类别相关，而且以识别图中内容为主，比如“图中的画是那个任务的代表作？”、“图中展现的场景是那个节日”。
            7. 答案是给定的标签或者是标签相关的。
            8. 不能仅凭问题就能得出答案，一定要理解并结合图片的内容才能得出答案。
            请按照下面的格式返回生成的问题和答案: {{"question": "此处为生成问题", "answer": "此处为答案"}}
            ### 让我们开始吧!
            类别：{question_class}
            标签：{label}
            """.strip()

prompt_rec_QA_wimg_v3 = """
            现在我给你提供一张图片和与该图片相关的标签，还有该标签所属的类别，请根据图片生成一个关联图片问题和对应的标准答案。生成的问题是根据图片可以提出的问题,而且这个问题的答案必须严格是图片中出现的实体,而且与给出的标签以及标签的类别相关
            生成的问题必须满足以下要求:
            1. 生成的问题必须可以用图片中出现的实体作为答案，且以识别图中内容为主，是不需要关联任何图片中实体以外的知识就可以回答的。例如,不要提问“图片中展现的运河位于哪个国家?”,因为这个问题的答案不是一个实体,而且答案也并不会出现在图片中。也不要问“图片中的晶体主要成分是什么?”,因为这个问题的答案从图片中也看不出来。也尽量不要询问“图片中的景色拍摄于哪个地区?”,这个问题从图片中也很难看出来。
            2. 所提出的问题必须有且只有一个明确且无争议的实体作为答案,且问题表述中不应存在任何形式的模糊性或歧义。例如,避免提问“图片中的是什么?”因为无法确定具体指的是什么东西,图片中可能有多个实体。
            3. 所提出的问题尽量避免是“图中物品是什么颜色？”、“图中物品是什么形状？”这样基础的问题，可以是“图中橙色墙壁的建筑是什么？”
            4. 避免同时询问两个问题,所提出的问题应该有且仅有一个具体的问题,不能够被拆分成两个问题,比如"图片中左上角和下方分别是什么东西?"不合适,因为这个问题相当于是同时问了两个问题,也会有两个答案。
            5. 如果问题的答案为英文,请给出中文翻译后的答案和括号里带上英文原名,格式如:雅各布·福格(Jakob Fugger)。
            6. 提出的问题要考虑标签所属的类别
            7. 答案是给定的标签或者是标签相关的内容。
            8. 提出的问题一定要理解并结合图片的内容才能得出答案。
            9. 请用简体中文返回结果,不要繁体中文。
            请按照下面的格式返回生成的问题和答案: {{"question": "此处为生成问题", "answer": "此处为答案"}}
            ### 让我们开始吧!
            标签：{label}
            标签类别：{label_class}
            """.strip()

prompt_rec_QA_wimg_v4 = """
            现在我给你提供一张图片和与该图片相关的标签，还有该标签所属的类别，请根据图片生成一个关联图片问题和对应的标准答案。生成的问题是根据图片可以提出的问题,而且这个问题的答案必须严格是图片中出现的实体,而且与给出的标签以及标签的类别相关
            生成的问题必须满足以下要求:
            1. 生成的问题必须可以用图片中出现的实体作为答案，且以识别图中内容为主，是不需要关联任何图片中实体以外的知识就可以回答的。例如,不要提问“图片中展现的运河位于哪个国家?”,因为这个问题的答案不是一个实体,而且答案也并不会出现在图片中。也不要问“图片中的晶体主要成分是什么?”,因为这个问题的答案从图片中也看不出来。
            2. 所提出的问题必须有且只有一个明确且无争议的实体作为答案,且问题表述中不应存在任何形式的模糊性或歧义。例如,避免提问“图片中的是什么?”因为无法确定具体指的是什么东西,图片中可能有多个实体。
            3. 所提出的问题尽量避免是“图中物品是什么颜色？”、“图中物品是什么形状？”这样基础的问题，可以是“图中橙色墙壁的建筑是什么？”
            4. 避免同时询问两个问题,所提出的问题应该有且仅有一个具体的问题,不能够被拆分成两个问题,比如"图片中左上角和下方分别是什么东西?"不合适,因为这个问题相当于是同时问了两个问题,也会有两个答案。
            5. 如果问题的答案为英文,请给出中文翻译后的答案和括号里带上英文原名,格式如:雅各布·福格(Jakob Fugger)。
            6. 提出的问题要考虑标签所属的类别
            7. 问题中不能带有标签，但是答案最好是标签相关的内容，也可以直接是给定的标签。
            8. 提出的问题一定要理解并结合图片的内容才能得出答案。
            9. 请用简体中文返回结果,不要繁体中文。
            请按照下面的格式返回生成的问题和答案: {{"question": "此处为生成问题", "answer": "此处为答案"}}
            ### 让我们开始吧!
            标签：{label}
            标签类别：{label_class}
            """.strip()

prompt_rec_QA_wimg_v4_en = """
            Now I provide you with an image and tag related to that image, as well as the category to which the tag belongs. Please generate an image-related question and corresponding standard answer based on the image. The generated question should be one that can be asked based on the image, and the answer to this question must strictly be an entity that appears in the image, and is related to the given tag and the tag's category.
            The generated question must meet the following requirements:
            1.The generated question must be answerable with entities that appear in the image, and should focus mainly on identifying content in the image, without requiring any knowledge beyond the entities in the image. For example, do not ask "Which country is the canal shown in the image located in?" because the answer to this question is not an entity, and the answer would not appear in the image. Also do not ask "What is the main component of the crystal in the image?" because the answer to this question cannot be seen from the image.
            2.The proposed question must have one and only one clear and unambiguous entity as the answer, and the question statement should not contain any form of ambiguity or uncertainty. For example, avoid asking "What is in the image?" because it's unclear what specifically is being referred to, and there may be multiple entities in the image.
            3.The proposed questions should avoid basic questions like "What color is the object in the image?" or "What shape is the object in the image?" Instead, they could be like "What is the building with orange walls in the image?"
            4.Avoid asking two questions simultaneously. The proposed question should have one and only one specific question that cannot be split into two questions. For example, "What are the things in the upper left corner and lower part of the image respectively?" is inappropriate because this question is equivalent to asking two questions at the same time and would have two answers.
            5.The proposed question should consider the category to which the tag belongs.
            6.The Questions cannot contain tag, but the answer should preferably be content related to the tag, or it can also be the given tag directly.
            7.The proposed question must require understanding and combining the image content to arrive at the answer.
            8.Please return the results in English.
            Please return the generated question and answer in the following format: {{"question": "Generated question here", "answer": "Answer here"}}
            ### Let's begin!
            Tag: {label}
            Tag Category: {label_class}
            """.strip()

prompt_rec_QA_woimg_v1 = """
            现在我给你提供一段对图片的描述，该描述带有与该图片相关的知识，还给定了生成的问题需要相关的类别,请根据图片生成一个关联图片问题和对应的标准答案。生成的问题是根据图片可以提出的问题,而且这个问题的答案必须严格同时既是图片中出现的实体,也是相关的文档、补充知识出现过的实体，此外生成的问题需与类别相关
            生成的问题必须满足以下要求:
             
            1. 生成的问题必须可以用图片中出现的实体作为答案,是不需要关联任何图片中实体以外的知识就可以回答的。例如,不要提问“图片中展现的运河位于哪个国家?”,因为这个问题的答案不是一个实体,而且答案也并不会出现在图片中。也避免提问“图片中的这张海报是谁设计的?”因为这个问题需要图片之外的知识,从图片中看不出来。也不要问“图片中的晶体主要成分是什么?”,因为这个问题的答案从图片中也看不出来。也尽量不要询问“图片中的景色拍摄于哪个地区?”,这个问题从图片中也很难看出来。
            2. 所提出的问题必须有且只有一个明确且无争议的实体作为答案,且问题表述中不应存在任何形式的模糊性或歧义。例如,避免提问“图片中的是什么?”因为无法确定具体指的是什么东西,图片中可能有多个实体。
            3. 避免同时询问两个问题,所提出的问题应该有且仅有一个具体的问题,不能够被拆分成两个问题,比如"图片中左上角和下方分别是什么东西?"不合适,因为这个问题相当于是同时问了两个问题,也会有两个答案。
            4. 如果问题的答案为英文,请给出中文翻译后的答案和括号里带上英文原名,格式如:雅各布·福格(Jakob Fugger)。
            5. 请用简体中文返回结果,不要繁体中文。
            6. 生成的问题需要与给定的类别相关
            请按照下面的格式返回生成的问题和答案: {{"question": "此处为生成问题", "answer": "此处为答案"}}
            ### 让我们开始吧!
            类别：{class}
            图片描述：{caption}
            """.strip()

prompt_know_QA_v1 = """
            现在我给你提供一个问答对和与该问答对相关的带有补充知识的图片描述,还有该问答对相关的类别,你需要在该问答对的基础上根据图片描述以及你自己知道的相关知识生成一个新的事实性问题和对应的标准答案,生成的问题必须以所提供的问答对中的答案开头进行提问，并且一定与给定的类别相关,生成的答案从图片描述和提供的问答对中的答案的相关知识获取。
            生成的问题必须满足以下要求: 
            1. 生成的问题必须关联到客观世界的知识,例如可以询问“罗伯特·德尼罗在1974年出演了哪一部电影?”不得构造涉及个人观点或感受相关的主观问题,如“你如何看待xxx?”。
            2. 所提出的问题必须有且只有一个明确且无争议的实体作为答案,且问题表述中不应存在任何形式的模糊性或歧义。例如,避免提问“罗伯特·德尼罗出演了哪一部电影?”因为无法确定是指哪一年出演的哪一部电影;“周汝昌最为人熟知的著作是哪个?”也是不合格问题,因为“最熟知”可能是有争议的;也不要问“美洲鳄通常长度是多少英寸?”因为这个问题的答案通常是一个范围, 比较模糊。同样不要提问“夜鹭主要分布在哪些区域?”因为这个问题通常会有多个答案,不清晰。还不要提问“机车是从哪里往哪里的?”因为机车可能是双向行驶的,答案可能有两个。
            3. 问题的答案应当是时间不变的,不会随着时间的推移而改变。例如,“美国的总统是谁?”就不是一个合适的问题,因为总统身份会随时间改变。
            4. 避免同时询问两个问题,所提出的问题应该有且仅有一个具体的问题,不能够被拆分成两个问题,比如"圣伯多禄这座大殿的建筑和广场设计者分别是谁?"不合适,因为这个问题相当于是同时问了两个问题,也会有两个答案。
            5. 问题应该具有一定的难度,以体现出一定的挑战性。例如:“电影《脱衣舞娘》是由同名小说改编的,该小说的作者是谁?”。
            6. 不要在提问的时候提供多余的信息,让问题在能得出确切答案的前提下提供尽量少的信息。绝对不要用类似这样的方式提问"德森卡火车站位于哪个国家的文尼察州?"。因为‘文尼察州’相当于提供了更多的信息。这个问题应该变成“德森卡火车站位于哪个国家?”。
            7. 如果问题的答案为英文,请给出中文翻译后的答案和括号里带上英文原名,格式如:雅各布·福格(Jakob Fugger)。
            8. 请用简体中文返回结果,不要繁体中文
            9. 生成的问题需要与给定的类别相关
            请按照下面的格式返回生成的问题和答案 : 
            {{"question": "此处为生成问题", "answer": "此处为答案"}} 
            ### 
            让我们开始吧!
            问答对：{QA_rec}
            类别：{question_class}
            图片描述：{caption}
            """.strip()

prompt_know_QA_v2 = """
            现在我给你提供一个问答对和与该问答对相关的带有补充知识的图片描述，还有该图片描述的标签，你需要在该问答对的基础上根据图片描述以及标签的的相关知识生成一个新的事实性问题和对应的标准答案,生成的问题必须以所提供的问答对中的答案开头进行提问，生成的答案从图片描述和标签相关知识获取。
            生成的问题必须满足以下要求: 
            1. 生成的问题必须关联到客观世界的知识,例如可以询问“罗伯特·德尼罗在1974年出演了哪一部电影?”不得构造涉及个人观点或感受相关的主观问题,如“你如何看待xxx?”。
            2. 所提出的问题必须有且只有一个明确且无争议的实体作为答案,且问题表述中不应存在任何形式的模糊性或歧义。例如,避免提问“罗伯特·德尼罗出演了哪一部电影?”因为无法确定是指哪一年出演的哪一部电影;“周汝昌最为人熟知的著作是哪个?”也是不合格问题,因为“最熟知”可能是有争议的;也不要问“美洲鳄通常长度是多少英寸?”因为这个问题的答案通常是一个范围, 比较模糊。同样不要提问“夜鹭主要分布在哪些区域?”因为这个问题通常会有多个答案,不清晰。还不要提问“机车是从哪里往哪里的?”因为机车可能是双向行驶的,答案可能有两个。
            3. 问题的答案应当是时间不变的,不会随着时间的推移而改变。例如,“美国的总统是谁?”就不是一个合适的问题,因为总统身份会随时间改变。但是“2010年的美国的总统是谁?”就是一个合规的问题。
            4. 避免同时询问两个问题,所提出的问题应该有且仅有一个具体的问题,不能够被拆分成两个问题,比如"圣伯多禄这座大殿的建筑和广场设计者分别是谁?"不合适,因为这个问题相当于是同时问了两个问题,也会有两个答案。
            5. 问题应该具有一定的难度,以体现出一定的挑战性。例如:“电影《脱衣舞娘》是由同名小说改编的,该小说的作者是谁?”。
            6. 不要在提问的时候提供多余的信息,让问题在能得出确切答案的前提下提供尽量少的信息。绝对不要用类似这样的方式提问"德森卡火车站位于哪个国家的文尼察州?"。因为‘文尼察州’相当于提供了更多的信息。这个问题应该变成“德森卡火车站位于哪个国家?”。
            7. 如果问题的答案为英文,请给出中文翻译后的答案和括号里带上英文原名,格式如:雅各布·福格(Jakob Fugger)。
            8. 请用简体中文返回结果,不要繁体中文
            请按照下面的格式返回生成的问题和答案: 
            {{"question": "此处为生成问题", "answer": "此处为答案"}} 
            ### 
            让我们开始吧!
            问答对：{QA_rec}
            标签：{label}
            图片描述：{caption}
            """.strip()

prompt_know_QA_v3 = """
            现在我给你提供一个问答对和与该问答对相关的带有标签补充知识的图片描述，还有该图片描述的标签和标签所属的类别，你需要在该问答对的基础上根据图片描述以及标签的相关知识生成一个新的事实性问题和对应的标准答案,生成的问题必须以所提供的问答对中的答案开头进行提问，生成的答案从图片描述和标签相关知识获取。
            生成的问题必须满足以下要求: 
            1. 生成的问题必须关联到客观世界的知识,例如可以询问“罗伯特·德尼罗在1974年出演了哪一部电影?”不得构造涉及个人观点或感受相关的主观问题,如“你如何看待xxx?”。
            2. 所提出的问题必须有且只有一个明确且无争议的实体作为答案,且问题表述中不应存在任何形式的模糊性或歧义。例如,避免提问“罗伯特·德尼罗出演了哪一部电影?”因为无法确定是指哪一年出演的哪一部电影;“周汝昌最为人熟知的著作是哪个?”也是不合格问题,因为“最熟知”可能是有争议的;也不要问“美洲鳄通常长度是多少英寸?”因为这个问题的答案通常是一个范围, 比较模糊。同样不要提问“夜鹭主要分布在哪些区域?”因为这个问题通常会有多个答案,不清晰。还不要提问“机车是从哪里往哪里的?”因为机车可能是双向行驶的,答案可能有两个。
            3. 生成的问题和答案可以参考标签的类别，但是不需要严格相关。
            4. 问题的答案应当是时间不变的,不会随着时间的推移而改变。例如,“美国的总统是谁?”就不是一个合适的问题,因为总统身份会随时间改变。但是“2010年的美国的总统是谁?”就是一个合规的问题。
            5. 避免同时询问两个问题,所提出的问题应该有且仅有一个具体的问题,不能够被拆分成两个问题,比如"圣伯多禄这座大殿的建筑和广场设计者分别是谁?"不合适,因为这个问题相当于是同时问了两个问题,也会有两个答案。
            6. 问题应该具有一定的难度,以体现出一定的挑战性。例如:“电影《脱衣舞娘》是由同名小说改编的,该小说的作者是谁?”。
            7. 不要在提问的时候提供多余的信息,让问题在能得出确切答案的前提下提供尽量少的信息。绝对不要用类似这样的方式提问"德森卡火车站位于哪个国家的文尼察州?"。因为‘文尼察州’相当于提供了更多的信息。这个问题应该变成“德森卡火车站位于哪个国家?”。
            8. 如果问题的答案为英文,请给出中文翻译后的答案和括号里带上英文原名,格式如:雅各布·福格(Jakob Fugger)。
            9. 请用简体中文返回结果,不要繁体中文
            请按照下面的格式返回生成的问题和答案: 
            {{"question": "此处为生成问题", "answer": "此处为答案"}} 
            ### 
            让我们开始吧!
            问答对：{QA_rec}
            标签：{label}
            标签类别：{label_class}
            图片描述：{caption}
            """.strip()

prompt_know_QA_v3_en = """
            Now I provide you with a Q&A pair and a picture description with labeled supplemental knowledge related to that Q&A pair, as well as the labels and categories of the picture description. You need to generate a new factual question and corresponding standard answer based on the Q&A pair, using the picture description and label-related knowledge. The generated question must begin with the answer from the provided Q&A pair.
            The generated question must meet the following requirements:
            1.The generated question must be related to objective world knowledge, for example, you can ask "What movie did Robert De Niro star in in1974?" You must not construct subjective questions involving personal opinions or feelings, such as "What do you think of xxx?"
            2.The proposed question must have one and only one clear and uncontroversial entity as the answer, and there should be no ambiguity or vagueness in the question formulation. For example, avoid asking "What movie did Robert De Niro star in?" because it's unclear which year or which movie is being referred to; "What is Zhou Ruchang's most well-known work?" is also an unqualified question because "most well-known" might be controversial; also don't ask "What is the usual length of American crocodiles in inches?" because the answer to this question is usually a range, which is vague. Similarly, don't ask "Which regions are night herons mainly distributed in?" because this question usually has multiple answers and is unclear. Also don't ask "Where does the locomotive go from and to?" because locomotives might run in both directions, so there could be two answers.
            3.The generated questions and answers can reference the categories of labels, but don't need to be strictly related.
            4.The answer to the question should be time-invariant and will not change over time. For example, "Who is the President of the United States?" is not a suitable question because the president's identity changes over time. But "Who was the President of the United States in 2010?" is a compliant question.
            5.Avoid asking two questions at the same time. The proposed question should have one and only one specific question that cannot be split into two questions. For example, "Who are the architect and plaza designer of St. Peter's Basilica respectively?" is inappropriate because this question is equivalent to asking two questions simultaneously and will have two answers.
            6.The question should have a certain level of difficulty to demonstrate some challenge. For example: "The movie 'Striptease' is adapted from a novel of the same name. Who is the author of that novel?"
            7.Don't provide redundant information when asking questions. Let the question provide as little information as possible while still being able to derive a definite answer. Never ask in a way like "Which country's Vinnytsia Oblast is Desenko railway station located in?" Because 'Vinnytsia Oblast' provides additional information. This question should become "Which country is Desenko railway station located in?"
            8.Please return the results in English.
            Please return the generated question and answer in the following format:
            {{"question": "Generated question here", "answer": "Answer here"}}
            ###
            Let's begin!
            Q&A pair: {QA_rec}
            Label: {label}
            Label category: {label_class}
            Picture description: {caption}
            """.strip()

prompt_know_QA_list_v1 = """
            现在我给你提供一个问答对和与该问答对相关的带有标签补充知识的图片描述，还有该图片描述的标签和标签所属的类别，你需要在该问答对的基础上根据图片描述以及标签的相关知识生成三个或三个以上不同的新的事实性问题和对应的标准答案,生成的问题必须以所提供的问答对中的答案开头进行提问，生成的答案从图片描述和标签相关知识获取。
            生成的问题必须满足以下要求: 
            1. 生成的问题必须关联到客观世界的知识,例如可以询问“罗伯特·德尼罗在1974年出演了哪一部电影?”不得构造涉及个人观点或感受相关的主观问题,如“你如何看待xxx?”。
            2. 所提出的问题必须有且只有一个明确且无争议的实体作为答案,且问题表述中不应存在任何形式的模糊性或歧义。例如,避免提问“罗伯特·德尼罗出演了哪一部电影?”因为无法确定是指哪一年出演的哪一部电影;“周汝昌最为人熟知的著作是哪个?”也是不合格问题,因为“最熟知”可能是有争议的;也不要问“美洲鳄通常长度是多少英寸?”因为这个问题的答案通常是一个范围, 比较模糊。同样不要提问“夜鹭主要分布在哪些区域?”因为这个问题通常会有多个答案,不清晰。还不要提问“机车是从哪里往哪里的?”因为机车可能是双向行驶的,答案可能有两个。
            3. 生成的问题和答案可以参考标签的类别，但是不需要严格相关。
            4. 问题的答案应当是时间不变的,不会随着时间的推移而改变。例如,“美国的总统是谁?”就不是一个合适的问题,因为总统身份会随时间改变。但是“2010年的美国的总统是谁?”就是一个合规的问题。
            5. 避免同时在一个问题中询问两个问题,所提出的问题应该有且仅有一个具体的问题,不能够被拆分成两个问题,比如"圣伯多禄这座大殿的建筑和广场设计者分别是谁?"不合适,因为这个问题相当于是同时问了两个问题,也会有两个答案。
            6. 生成的各个问题的角度需要不同，即需要不同方面的知识来回答，同时问题应该具有一定的难度,以体现出一定的挑战性。例如:“电影《脱衣舞娘》是由同名小说改编的,该小说的作者是谁?”，“电影《脱衣舞娘》是什么时候上映的?”，“电影《脱衣舞娘》中的女主角叫什么名字?”
            7. 不要在提问的时候提供多余的信息,让问题在能得出确切答案的前提下提供尽量少的信息。绝对不要用类似这样的方式提问"德森卡火车站位于哪个国家的文尼察州?"。因为‘文尼察州’相当于提供了更多的信息。这个问题应该变成“德森卡火车站位于哪个国家?”。
            8. 如果问题的答案为英文,请给出中文翻译后的答案和括号里带上英文原名,格式如:雅各布·福格(Jakob Fugger)。
            9. 请用简体中文返回结果,不要繁体中文
            ###
            请按照下面的格式返回生成的问题和答案: 
            [{{"question": "此处为生成问题", "answer": "此处为答案"}}, {{"question": "此处为生成问题", "answer": "此处为答案"}}, ...] 
            ### 
            让我们开始吧!
            问答对：{QA_rec}
            标签：{label}
            标签类别：{label_class}
            图片描述：{caption}
            """.strip()

prompt_know_QA_list_v1_en = """
            Now I will provide you with a Q&A pair and an image description with labeled supplementary knowledge related to that Q&A pair, along with the labels and their categories. You need to generate three or more different new factual questions and corresponding standard answers based on the Q&A pair, using the image description and label-related knowledge. The generated questions must begin by asking about the answer provided in the given Q&A pair, and the generated answers should be obtained from the image description and label-related knowledge.
            The generated questions must meet the following requirements:
            1.The generated questions must relate to objective world knowledge. For example, you can ask "What movie did Robert De Niro star in in 1974?" You must not construct subjective questions involving personal opinions or feelings, such as "What do you think about xxx?"
            2.The proposed questions must have exactly one clear and undisputed entity as the answer, and the question formulation should not contain any form of ambiguity or vagueness. For example, avoid asking "What movie did Robert De Niro star in?" because it's unclear which year or which specific movie is being referenced; "What is Zhou Ruchang's most well-known work?" is also an unqualified question because "most well-known" could be controversial; also don't ask "What is the typical length of an American crocodile in inches?" because the answer is usually a range, which is vague. Similarly, don't ask "In which regions are night herons mainly distributed?" because this question usually has multiple answers and is unclear. Also don't ask "Where does the locomotive go from and to?" because locomotives may run in both directions, potentially having two answers.
            3.The generated questions and answers can reference the label categories but don't need to be strictly related.
            4.The answers to questions should be time-invariant and not change over time. For example, "Who is the President of the United States?" is not a suitable question because the president's identity changes over time. However, "Who was the President of the United States in2010?" is a compliant question.
            5.Avoid asking two questions simultaneously in one question. The proposed question should have exactly one specific question that cannot be split into two questions. For example, "Who were the architect and square designer of St. Peter's Basilica respectively?" is inappropriate because this question is equivalent to asking two questions simultaneously and would have two answers.
            6.The generated questions should have different perspectives, requiring different aspects of knowledge to answer, and the questions should have a certain level of difficulty to demonstrate some challenge. For example: "The movie 'Striptease' was adapted from a novel of the same name. Who is the author of that novel?", "When was the movie 'Striptease' released?", "What is the name of the female protagonist in the movie 'Striptease'?"
            7.Don't provide unnecessary information when asking questions. Make the questions provide as little information as possible while still being able to derive a definitive answer. Never ask in a way like "In which country is Desenca train station located in Vinnytsia Oblast?" Because 'Vinnytsia Oblast' provides additional information. This question should become "In which country is Desenca train station located?"
            8.Please return results in English.
            ###
            Please return the generated questions and answers in the following format:
            [{{"question": "Generated question here", "answer": "Answer here"}}, {{"question": "Generated question here", "answer": "Answer here"}}, ...]
            ###
            Let's begin!
            Q&A pair: {QA_rec}
            Labels: {label}
            Label categories: {label_class}
            Image description: {caption}
            """.strip()

prompt_final_QA_v1 = """
            现在我给你提供两个问答对,他们是递进的关系,第二个问答对是根据第一个问答对得到的。你需要修改并合成这两个问答对的问题来生成一个新的流畅的事实性问题,以第一个问题的一部分开头,以第二个问题的一部分结尾。生成的问题必须不能出现第一个问答对的答案,能以第二个问答对的答案作为回答。
            生成的问题必须满足以下要求: 
            1. 生成的问题必须严格和第一个问答对的答案相关,需要达到得不到第一个问答对的答案就无法正确回答问题的程度。例如可以询问“图片中的湖泊位于土耳其的哪个省?”而不能够询问“图片中的湖泊所在的七湖国家公园位于土耳其的哪个省?”因为这个问题不需要知道第一个问答对的答案就能够回答。
            2. 确保新生成的问题流畅而简洁。
            请按照下面的格式返回生成的问题和答案 : 
            {{"question": "此处为生成问题", "answer": "此处为答案"}}
            ### 让我们开始吧!
            第一个问答对：{QA_rec}
            第一个问答对：{QA_know}
            """.strip()

prompt_final_QA_v2 = """
            现在我给你两个问答对和该问答对的标签,两个问答对是递进的关系,第二个问答对是根据第一个问答对得到的。你需要修改并合成这两个问答对的问题来生成一个新的流畅的事实性问题。
            生成的问题必须满足以下要求: 
            1. 生成的问题必须严格和第一个问答对的答案相关，需要达到得不到第一个问答对的答案就无法正确回答问题的程度。例如可以询问“图片中的湖泊位于土耳其的哪个省?”而不能够询问“图片中的湖泊所在的七湖国家公园位于土耳其的哪个省?”因为这个问题不需要知道第一个问答对的答案就能够回答。
            2. 生成的问题必须不能出现第一个问答对的答案，能以第二个问答对的答案作为回答。
            3. 生成的问题不能包含给出的标签，不管是中文还是英文
            4. 确保新生成的问题流畅而简洁。
            请按照下面的格式返回生成的问题和答案 : 
            {{"question": "此处为生成问题", "answer": "此处为答案"}}
            ### 让我们开始吧!
            标签：{label}
            第一个问答对：{QA_rec}
            第一个问答对：{QA_know}
            """.strip()

prompt_final_QA_v3 = """
            现在我给你两个问答对和该问答对的标签,两个问答对是递进的关系,第二个问答对是根据第一个问答对得到的。你需要修改并合并这两个问答对的问题来生成一个新的流畅的事实性问题。
            生成的问题必须满足以下要求: 
            1. 生成的问题必须严格和第一个问答对的答案相关，需要达到得不到第一个问答对的答案就无法正确回答问题的程度。例如可以询问“图片中的湖泊位于土耳其的哪个省?”而不能够询问“图片中的湖泊所在的七湖国家公园位于土耳其的哪个省?”因为这个问题不需要知道第一个问答对的答案就能够回答。
            2. 生成的问题必须不能出现第一个问答对的答案，能以第二个问答对的答案作为回答。
            3. 生成的问题不能包含给出的标签，不管是中文还是英文
            4. 确保新生成的问题流畅而简洁。
            5. 避免同时询问两个问题,合并的问题应该有且仅有一个具体的问题
            请按照下面的格式返回生成的问题和答案 : 
            {{"question": "此处为生成问题", "answer": "此处为答案"}}
            ### 让我们开始吧!
            标签：{label}
            第一个问答对：{QA_rec}
            第一个问答对：{QA_know}
            """.strip()

prompt_final_QA_v3_en = """
            Now I will give you two question-answer pairs and their labels. The two question-answer pairs have a progressive relationship, where the second question-answer pair is derived from the first one. You need to modify and synthesize the questions from these two question-answer pairs to generate a new, fluent factual question.
            The generated question must meet the following requirements:
            1.The generated question must be strictly related to the answer of the first question-answer pair, to the extent that you cannot correctly answer the question without obtaining the answer from the first question-answer pair. For example, you can ask "Which province in Turkey is the lake in the picture located in?" but you cannot ask "Which province in Turkey is the Seven Lakes National Park where the lake in the picture is located?" because this question can be answered without knowing the answer to the first question-answer pair.
            2.The generated question must not contain the answer from the first question-answer pair, and should be answerable with the answer from the second question-answer pair.
            3.The generated question cannot contain the given labels, whether in Chinese or English.
            4.Ensure the newly generated question is fluent and concise.
            5.Avoid asking two questions simultaneously; the merged question should have one and only one specific question.
            Please return the generated question and answer in the following format:
            {{"question": "Generated question here", "answer": "Answer here"}}
            Let's begin!
            Label: {label}
            First question-answer pair: {QA_rec}
            Second question-answer pair: {QA_know}
            """.strip()

prompt_final_QA_cot_list_v1 = """
            现在我给你一个问答对和多个问答对组成的列表，还有所有问答对对应的标签,第一个问答对和之后列表里的问答对是递进的关系,列表里的所有问答对都是根据第一个问答对得到的。你需要分别修改并合并第一个问答对和列表里的问答对的问题来生成一个新的流畅的事实性问题。
            生成的问题必须满足以下要求: 
            1. 生成的问题必须严格和第一个问答对的答案相关，需要达到得不到第一个问答对的答案就无法正确回答问题的程度。例如可以询问“图片中的湖泊位于土耳其的哪个省?”而不能够询问“图片中的湖泊所在的七湖国家公园位于土耳其的哪个省?”因为这个问题不需要知道第一个问答对的答案就能够回答。
            2. 生成的问题必须不能出现第一个问答对的答案，能以第二个问答对的答案作为回答。
            3. 生成的问题不能包含给出的标签，不管是中文还是英文
            4. 确保新生成的问题流畅而简洁。
            5. 避免同时询问两个问题,合并的问题应该有且仅有一个具体的问题
            请按照下面的格式返回生成的问题和答案 : 
            {{"question": "此处为生成问题", "answer": "此处为答案"}}
            ### 让我们开始吧!
            标签：{label}
            第一个问答对：{QA_rec}
            第一个问答对：{QA_know}
            """.strip()

prompt_final_QA_cot_v1 = """
            现在我给你两个问答对和该问答对的标签,两个问答对是递进的关系,第二个问答对是根据第一个问答对得到的。你需要修改并合并这两个问答对的问题来生成一个新的流畅的事实性问题。
            生成的问题必须满足以下要求: 
            1. 生成的问题必须严格和第一个问答对的答案相关，需要达到得不到第一个问答对的答案就无法正确回答问题的程度。例如可以询问“图片中的湖泊位于土耳其的哪个省?”而不能够询问“图片中的湖泊所在的七湖国家公园位于土耳其的哪个省?”因为这个问题不需要知道第一个问答对的答案就能够回答。
            2. 生成的问题必须不能出现第一个问答对的答案，能以第二个问答对的答案作为回答。但是因为两个问答对是递进关系，所以新生成的答案应该包含简单的推理过程。
            3. 生成的问题不能包含给出的标签，不管是中文还是英文
            4. 确保新生成的问题流畅而简洁。
            5. 避免同时询问两个问题,合并的问题应该有且仅有一个具体的问题
            请按照下面的格式返回生成的问题和答案 : 
            {{"question": "此处为生成问题", "answer": "此处为答案"}}
            ### 示例
            标签：人物-娱乐体育类
            第一个问答对：{{"question": "图中这位额头有伤痕的女演员是谁？", "answer": "范冰冰"}}
            第二个问答对：{{"question": "范冰冰凭借哪部电影获得了圣塞巴斯蒂安国际电影节最佳女主角银贝壳奖？", "answer": "《我不是潘金莲》"}}
            最终合成问答对：{{"question": "图中这位额头有伤痕的女演员凭借哪部电影获得了圣塞巴斯蒂安国际电影节最佳女主角银贝壳奖？", "answer": "图中这位额头有伤痕的女演员是范冰冰，她凭借《我不是潘金莲》获得了该奖项"}}
            ### 让我们开始吧!
            标签：{label}
            第一个问答对：{QA_rec}
            第一个问答对：{QA_know}
            最终合成问答对：
            """.strip()

prompt_final_QA_cot_v1_en = """
            Now I will give you two question-answer pairs and their label. The two Q&A pairs have a progressive relationship, where the second Q&A pair is derived from the first one. You need to modify and merge the questions from these two Q&A pairs to generate a new fluent factual question.
            The generated question must meet the following requirements:
            1. The generated question must be strictly related to the answer of the first Q&A pair, to the extent that it cannot be correctly answered without knowing the answer to the first Q&A pair. For example, you can ask "Which province in Turkey is the lake in the image located in?" rather than "Which province in Turkey is the Seven Lakes National Park where the lake in the image is located?" because this question can be answered without knowing the answer to the first Q&A pair.
            2. The generated question must not contain the answer from the first Q&A pair, but should be answerable with the answer from the second Q&A pair. However, since the two Q&A pairs are progressive, the newly generated answer should include a simple reasoning process.
            3. The generated question cannot contain the given label, whether in Chinese or English.
            4. Ensure the newly generated question is fluent and concise.
            5. Avoid asking two questions simultaneously; the merged question should have one and only one specific question.
            Please return the generated question and answer in the following format:
            {{"question": "Generated question here", "answer": "Answer here"}}
            ### Example
            Label: 人物-娱乐体育类
            First Q&A pair: {{"question": "Who is this actress with a scar on her forehead in the image?", "answer": "Fan Bingbing"}}
            Second Q&A pair: {{"question": "For which movie did Fan Bingbing win the Silver Shell Award for Best Actress at the San Sebastián International Film Festival?", "answer": "I Am Not Madame Bovary"}}
            Final merged Q&A pair: {{"question": "For which movie did this actress with a scar on her forehead in the image win the Silver Shell Award for Best Actress at the San Sebastián International Film Festival?", "answer": "This actress with a scar on her forehead in the image is Fan Bingbing, and she won this award for'I Am Not Madame Bovary'"}}

            ### Let's begin!
            Label: {label}
            First Q&A pair: {QA_rec}
            Second Q&A pair: {QA_know}
            Final merged Q&A pair:
            """.strip()

prompt_QA_rule_filter_v1 = """
            你是一个数据质量检查员,现在需要你检查下面根据图片生成的问题和对应的答案是否满足以下要求: 
            1. 生成的问题必须严格和图片相关,需要达到没有图片就无法正确得出答案的程度。例如可以询问“图中的动物习惯生活在什么环境当中?”而不能够询问“鸵鸟习惯生活在什么环境中?”因为这个问题不需要看图片就能够回答。
            2. 生成的问题不能够仅依靠图片就能够得到答案,例如可以询问“图中展现的蝴蝶属于哪个科?”但是不能询问“图中展现的蝴蝶翅膀是什么颜色?”因为这个问题仅仅依靠图片就能够回答,我们要让问题需要结合外部知识才可以回答。
            3. 生成的问题必须关联到客观世界的知识,例如可以询问“图片中的人物在1974年出演了哪一部电影?”不得构造涉及个人观点或感受相关的主观问题,如“你如何看待xxx?”。
            4. 所提出的问题必须有且只有一个明确且无争议的实体作为答案,且问题表述中不应存在任何形式的模糊性或歧义。例如,避免提问“图片中的人物出演了哪一部电影?”因为无法确定是指哪一年出演的哪一部电影;同样不要问“图片中的这类人身体的特点是什么?”因为这个问题过于模糊,没有明确的答案。“图中作家最为人熟知的著作是哪个?”也是不合格问题,因为“最熟知”可能是有争议的;也不要问“图中的这种动物通常长度是多少英寸?”因为这个问题的答案通常是一个范围,比较模糊。同样不要提问“图中的鸟类主要分布在哪些区域?”因为这个问题通常会有多个答案,不清晰。还不要提问“图中的机车是从哪里往哪里的?”因为机车可能是双向行驶的,答案可能有两个。
            5. 答案应当是时间不变的,不会随着时间的推移而改变。例如,“图片中这个国家的总统是谁?”就不是一个合适的问题, 因为总统身份会随时间改变。
            6. 避免同时询问两个问题,所提出的问题应该有且仅有一个具体的问题,不能够被拆分成两个问题,比如"图片中这座大殿的建筑和广场设计者分别是谁?"不合适,因为这个问题相当于是同时问了两个问题,也会有两个答案。
            如果问题不合格则解释并输出“【否】”, 如果问题合格则直接输出“【是】”
            #### 
            如果问题不合格则输出原因并最后输出“【否】”, 如果问题合格则直接输出“【是】”,注意如果认为问题不合格需要输出原因
            让我们开始吧!
            问题：{question}
            答案：{answer}
            """.strip()

prompt_QA_rule_filter_v2 = """
            你是一个数据质量检查员,现在需要你检查下面根据图片生成的问题和对应的答案是否满足以下要求: 
            1. 生成问题的答案需要结合图片中的信息才能正确得出。例如可以询问“图中的动物习惯生活在什么环境当中?”而不能够询问“鸵鸟习惯生活在什么环境中?”因为这个问题不需要看图片就能够回答。
            2. 生成的问题不能够仅依靠图片就能够得到答案,例如可以询问“图中展现的蝴蝶属于哪个科?”但是不能询问“图中展现的蝴蝶翅膀是什么颜色?”因为这个问题仅仅依靠图片就能够回答,我们要让问题需要结合外部知识才可以回答。
            3. 生成的问题必须关联到客观世界的知识,例如可以询问“图片中的人物在1974年出演了哪一部电影?”不得构造涉及个人观点或感受相关的主观问题,如“你如何看待xxx?”。
            4. 所提出的问题必须有且只有一个明确且无争议的实体作为答案,且问题表述中不应存在任何形式的模糊性或歧义。例如,避免提问“图片中的人物出演了哪一部电影?”因为无法确定是指哪一年出演的哪一部电影;同样不要问“图片中的这类人身体的特点是什么?”因为这个问题过于模糊,没有明确的答案。“图中作家最为人熟知的著作是哪个?”也是不合格问题,因为“最熟知”可能是有争议的;也不要问“图中的这种动物通常长度是多少英寸?”因为这个问题的答案通常是一个范围,比较模糊。同样不要提问“图中的鸟类主要分布在哪些区域?”因为这个问题通常会有多个答案,不清晰。还不要提问“图中的机车是从哪里往哪里的?”因为机车可能是双向行驶的,答案可能有两个。
            5. 答案应当是时间不变的,不会随着时间的推移而改变。例如,“图片中这个国家的总统是谁?”就不是一个合适的问题, 因为总统身份会随时间改变。
            6. 避免同时询问两个问题,所提出的问题应该有且仅有一个具体的问题,不能够被拆分成两个问题,比如"图片中这座大殿的建筑和广场设计者分别是谁?"不合适,因为这个问题相当于是同时问了两个问题,也会有两个答案。
            如果问题不合格则解释并输出“【否】”, 如果问题合格则直接输出“【是】”
            #### 
            如果问题不合格则输出原因并最后输出“【否】”, 如果问题合格则直接输出“【是】”,注意如果认为问题不合格需要输出原因
            让我们开始吧!
            问题：{question}
            答案：{answer}
            """.strip()

prompt_QA_rule_filter_v3 = """
            你是一个数据质量检查员,现在需要你检查下面根据图片生成的问题和对应的答案是否满足以下要求:  
            1. 生成问题的答案需要结合图片中的信息才能正确得出。例如可以询问“图中的动物习惯生活在什么环境当中?”而不能够询问“鸵鸟习惯生活在什么环境中?”因为这个问题不需要看图片就能够回答。
            2. 生成的问题不能够仅依靠图片就能够得到答案,答案需要结合外部知识才能得到,例如可以询问“图中展现的蝴蝶属于哪个科?”但是不能询问“图中展现的蝴蝶翅膀是什么颜色?”因为这个问题仅仅依靠图片就能够回答,我们要让问题需要结合外部知识才可以回答。
            3. 生成的问题必须关联到客观世界的知识,例如可以询问“图片中的人物在1974年出演了哪一部电影?”不得构造涉及个人观点或感受相关的主观问题,如“你如何看待xxx?”。
            4. 所提出的问题必须有且只有一个明确且无争议的实体作为答案,且问题表述中不应存在任何形式的模糊性或歧义。例如,避免提问“图片中的人物出演了哪一部电影?”因为无法确定是指哪一年出演的哪一部电影;同样不要问“图片中的这类人身体的特点是什么?”因为这个问题过于模糊,没有明确的答案。“图中作家最为人熟知的著作是哪个?”也是不合格问题,因为“最熟知”可能是有争议的;也不要问“图中的这种动物通常长度是多少英寸?”因为这个问题的答案通常是一个范围,比较模糊。同样不要提问“图中的鸟类主要分布在哪些区域?”因为这个问题通常会有多个答案,不清晰。还不要提问“图中的机车是从哪里往哪里的?”因为机车可能是双向行驶的,答案可能有两个。
            5. 答案应当是时间不变的,不会随着时间的推移而改变。例如,“图片中这个国家的总统是谁?”就不是一个合适的问题, 因为总统身份会随时间改变。
            6. 避免同时询问两个问题,所提出的问题应该有且仅有一个具体的问题,不能够被拆分成两个问题,比如"图片中这座大殿的建筑和广场设计者分别是谁?"不合适,因为这个问题相当于是同时问了两个问题,也会有两个答案。
            按照满足要求的程度，给出1-3分的评价:
            - **3分(完全合格)**: 完全满足所有要求
            - **2分(勉强合格)**: 虽然不满足所有要求，但是满足要求4、5、6，即问题只有一个答案且不会随着时间的推移而改变，没有出现两个问题
            - **1分(不合格)**: 只要不满足4、5、6中的任一要求就是不合格，即出现了由多个答案、答案会随时间变化、有两个问题任一一个就为不合格
            #### 输出格式
            请给出简要理由后，严格按照以下格式输出分数：
            合格分数:[分数]
            #### 
            让我们开始吧!
            问题：{question}
            答案：{answer}
            """.strip()

prompt_QA_rule_filter_v3_en = """
            You are a data quality inspector. Now you need to check whether the questions and corresponding answers generated from the images below meet the following requirements:
            1.The answers to the generated questions need to be correctly derived by combining the information in the image. For example, you can ask "What environmentdo the animals in the image habitually live in?" but you cannot ask "What environment do ostriches habitually live in?" because this question can be answered without looking at the image.
            2.The generated questions cannot be answered solely by relying on the image; the answers need to be obtained by combining external knowledge. For example, you can ask "What family does the butterfly shown in the image belong to?" but you cannot ask "What color are the wings of the butterfly shown in the image?" because this question can be answered merely by looking at the image. We want questions that require combining external knowledge to answer.
            3.The generated questions must be related to objective world knowledge. For example, you can ask "What movie did the character in the image star in in 1974?" You must not construct subjective questions involving personal opinions or feelings, such as "What do you think of xxx?"
            4.The proposed question must have one and only one clear and undisputed entity as the answer, and there should be no ambiguity or vagueness in the question statement. For example, avoid asking "What movie did the character in the image star in?" because it's unclear which year or which specific movie is being referred to. Similarly, don't ask "What are the physical characteristics of this type of person in the image?" because this question is too vague and has no clear answer. "What is the most well-known work of the author in the image?" is also an unqualified question because "most well-known" may be controversial. Also don't ask "How many inches long is this type of animal in the image usually?" because the answer to this question is usually a range, which is ambiguous. Similarly, don't ask "In which regions are the birds in the image mainly distributed?" because this question usually has multiple answers and is unclear. Also don't ask "Where is the locomotive in the image going from and to?" because locomotives may operate in both directions, and there may be two answers.
            5.The answer should be time-invariant and will not change over time. For example, "Who is the president of this country in the image?" is not an appropriate question because the president's identity changes over time.
            6.Avoid asking two questions simultaneously. The proposed question should have one and only one specific question that cannot be split into two questions. For example, "Who are the architects of the main hall and the plaza designer in the image respectively?" is inappropriate because this question is equivalent to asking two questions simultaneously and will have two answers.
            According to the degree of meeting the requirements, give a score of 1-3points:
            3 points (fully qualified): Completely meets all requirements
            2 points (barely qualified): Although not meeting all requirements, it meets requirements 4, 5, and 6, i.e., the question has only one answer, does not change over time, and there are no two questions
            1 point (unqualified): Unqualified if it fails to meet any one of requirements 4, 5, or6, i.e., having multiple answers, answers changing over time, or having two questions
            #### Output Format
            Please give your brief reasoning first, then strictly output the score in the following format:
            Qualification Score: [Score]
            ####
            Let's begin!
            Question: {question}
            Answer: {answer}
            """.strip()

prompt_image_relevance_filter_v1 = """
            你是一个数据质量检查员,现在给你一张图片和该图片对应的标签，还有对这张图片的介绍以及标签知识，需要依据图片的介绍和标签知识判断图片和标签的相关性，并按以下标准打分: 
            - **5分(完全相关)**: 图片内容与标签完全匹配，图片中直接包含了标签内容
            - **4分(高度相关)**: 图片内容与标签密切相关，图片中的内容直接与标签相关，可能是标签的作品、组成部分等
            - **3分(中等相关)**: 图片内容与标签有一定关联，图片中的内容并不直接与标签相关，但是可以通过图片内容联想到标签
            - **2分(低度相关)**: 图片内容与标签存在微弱关联，需要推理才能建立联系
            - **1分(完全不相关)**: 图片内容与标签没有任何关联
            #### 分析要求
            1. 仔细观察图片中的所有可见元素（物体、人物、场景、文字等）
            2. 结合提供的图片介绍和标签知识知识进行综合判断
            3. 只输出1-5之间的整数分数（包括1和5）
            #### 输出格式
            请给出简要理由后，严格按照以下格式输出分数：
            相关性分数:[分数]
            #### 让我们开始吧!
            图片介绍和标签知识：{caption}
            标签：{label}
            """.strip()

prompt_image_relevance_filter_v1_en = """
            You are a data quality inspector. Now you are given an image and its corresponding label, along with an introduction to the image and label knowledge. You need to judge the relevance between the image and label based on the image introduction and label knowledge, and score according to the following criteria:
            - **5 points (Completely Relevant)**: The image content completely matches the label, and the image directly contains the label content
            - **4 points (Highly Relevant)**: The image content is closely related to the label, the content in the image is directly related to the label, and may be works or components of the label
            - **3 points (Moderately Relevant)**: The image content has some association with the label, the content in the image is not directly related to the label, but the label can be associated through the image content
            - **2 points (Slightly Relevant)**: The image content has weak association with the label, requiring reasoning to establish a connection
            - **1 point (Completely Irrelevant)**: The image content has no association with the label
            #### Analysis Requirements
            1.Carefully observe all visible elements in the image (objects, people, scenes, text, etc.)
            2.Make comprehensive judgments by combining the provided image introduction and label knowledge
            3.Only output integer scores between 1-5 (including1 and 5)
            #### Output Format
            Please give a brief reason first, then strictly output the score in the following format:
            Relevance Score: [Score]
            #### Let's begin!
            Image introduction and label knowledge: {caption}
            Label: {label}
            """.strip()

prompt_trans_v1 = """
            你是一个智能翻译助手，需要将给出的答案翻译成中文。我会给你一个问题和对应的答案，请按以下规则处理：
            ### 判断规则：
            1. 如果问题是要求识别图中文字的类型，则直接返回原答案
            2. 如果答案本身已经全为中文，则直接返回原答案
            3. 如果答案是人名、地名、作品名等，则返回翻译后的答案和括号里带上原始答案，格式如:雅各布·福格(Jakob Fugger)
            4. 对于规则以外的情况，基于上述规则的理解自行判断
            ### 输出要求：
            - 按规则输出
            - 不要添加任何解释或说明
            ### 请处理以下内容：
            问题：{question}
            答案：{answer}
            """.strip()

prompt_trans_v1_en = """
            You are an intelligent translation assistant， need to translate the given answer into English. I will give you a question and its corresponding answer, please process them according to the following rules:
            ### Judgment Rules:
            1. If the question asks to identify the type of text in an image, return the original answer directly
            2. If some of the nouns in the answer are strongly related to Chinese culture, you can mark the original Chinese name, the format is as follows, Bao'an knives (保安腰刀)
            3. Except for rule 1 and 2, the translated answers must all be in English
            4. If the answer is already in English, return to the original answer directly
            5. For cases outside the rules, make your own judgment based on the understanding of the above rules
            ### Output Requirements:
            - Output according to the rules
            - Do not add any explanations or descriptions
            ### Please process the following content:
            Question: {question}
            Answer: {answer}
            """.strip()