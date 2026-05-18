import json
import re
import requests
import gradio as gr

# ============================================================
# First Voice
# Local-first narrative reframing with Gemma 4
# Submission for The Gemma 4 Good Hackathon
# License: CC BY 4.0
# Author: Cynthia Tseng
# Kaggle: @littlebeastai
#
# Product notes:
# 1. Layered narrative reframing workflow.
# 2. The core result page keeps the emotional peak and main insight.
# 3. Resume, interview, portfolio, social post, AI collaboration method,
#    and shortcut table are placed in the second layer to reduce overload.
# ============================================================

TITLE = "First Voice"
SUBTITLE = "Local-first narrative reframing with Gemma"

OLLAMA_MODEL = "gemma4:e4b"
OLLAMA_URL = "http://localhost:11434/api/generate"

ENTRY_QUESTION = "工作上，什麼事情卡住、混亂或沒人知道怎麼辦時，大家通常會找你？"


# ============================================================
# 五大工作行為模式
# 注意：這不是人格分類，也不是職涯測驗。
# 這裡的分類只是用來理解「使用者在工作中反覆被依賴的功能」。
# ============================================================

CATEGORIES = {
    "coordination": {
        "label": "幫大家把事情串起來的人",
        "description": "你常被找來釐清狀況、整理不同人的說法，讓事情重新可以往下走。",
        "questions": [
            "這類事情發生時，你通常會先找誰確認？為什麼？",
            "你通常怎麼判斷，現在卡住的是人的理解、溝通，還是事情本身？"
        ],
    },
    "technical": {
        "label": "很快看懂問題的人",
        "description": "你常被找來判斷問題在哪裡，尤其是別人看不出原因或不知道怎麼開始時。",
        "questions": [
            "別人卡住時，你通常會先看哪個線索來判斷問題？",
            "有沒有哪一類問題，你通常比別人更快看出狀況？"
        ],
    },
    "organization": {
        "label": "把混亂整理清楚的人",
        "description": "你常被找來把零散資訊、流程、文件或工作順序整理成可以執行的樣子。",
        "questions": [
            "你最常把哪一種混亂整理成清楚的步驟？",
            "你整理事情時，通常會先分出哪些類別或順序？"
        ],
    },
    "mentoring": {
        "label": "讓別人能順利做事的人",
        "description": "你常被找來教人、帶人、補說明，讓別人比較知道該怎麼做。",
        "questions": [
            "別人不會做或不敢做時，你通常怎麼讓他開始動起來？",
            "你最常幫新人或同事補上哪一種理解？"
        ],
    },
    "stabilization": {
        "label": "出事時會被找來穩住局面的人",
        "description": "你常被找來處理突發狀況、客訴、衝突或現場失控的問題。",
        "questions": [
            "這類狀況發生時，你通常會先確認哪一件事，讓現場可以先穩下來？",
            "你怎麼判斷現在最需要先處理的是資訊、責任、情緒，還是下一步行動？"
        ],
    },
}


# ============================================================
# 分類器 Prompt
# 這一步只負責判斷「工作行為模式」，不是推薦職業。
# ============================================================

CLASSIFIER_PROMPT = """
你是一個工作經驗分析助手。

你的任務：
根據使用者的回答，判斷他在工作中最常被依賴的功能類型。

重要限制：
這不是職涯測驗。
不要推薦職業。
不要判斷人格。
只判斷使用者描述中最明顯的「工作行為模式」。

只能從以下五個代號中選一個：

1. coordination
意思：常處理溝通、協作、跨部門、多人意見、資訊串聯、責任不清、流程卡住後重新推動。
如果回答中同時出現「跨部門」「誰負責」「下一步」「說法不同」「找誰確認」「流程卡住」，通常優先判斷為 coordination。

2. technical
意思：常處理技術、系統、工具、操作、錯誤判斷、問題排查、資料或設備問題。

3. organization
意思：常處理文件、流程、分類、規則、排程、資料整理、把混亂變清楚。
如果回答重點是把資料、文件、步驟、規則整理清楚，通常判斷為 organization。

4. mentoring
意思：常處理教學、帶新人、說明、陪同事理解流程、讓別人學會做事。

5. stabilization
意思：常處理危機、客訴升級、情緒爆炸、突發狀況、現場失控、緊急收拾局面。
注意：只有提到「客訴」或「客戶抱怨」不一定是 stabilization。
必須出現明確的失控、緊急、情緒爆炸、衝突升級、現場壓不住，才優先判斷為 stabilization。

請只輸出 JSON，不要輸出其他文字。

格式如下：
{
  "category": "coordination",
  "reason": "用一句話說明判斷原因"
}
"""


# ============================================================
# 核心結果 Prompt
# 主結果只保留 First Voice 的情緒峰值與核心理解。
# ============================================================

CORE_RESULT_PROMPT_TEMPLATE = """
你是 First Voice，一個 local-first narrative reframing tool。

你的任務不是替使用者推薦職業。
你的任務不是產生履歷、面試稿、作品集或社群貼文。
你的任務是先幫使用者看見：
他長期反覆在做的事情，其實是一種能力。

這一階段只產出核心理解，不產出工具層內容。
不要輸出履歷 bullet。
不要輸出面試稿。
不要輸出作品集。
不要輸出 LinkedIn 或 Threads。
不要輸出 AI prompt。
不要輸出快捷指令表。

請牢記 First Voice 的核心句：
「你不是在做雜事，你是在把混亂變成別人可以前進的路。」

請使用繁體中文。
請使用台灣常用語氣。
請避免空泛鼓勵。
請不要把使用者貼上固定標籤。
請不要寫得像心理測驗。
請不要寫成職涯推薦工具。
請不要替使用者決定未來。
請不要過度肯定。
請不要使用使用者指定的禁用詞。若不確定，改用台灣常見說法。

重要限制：
1. 不要使用「非常重要」「很棒」「很厲害」「天生」「命定」「完美」這類誇張語氣。
2. 不要使用「資訊流」「行動路徑」「系統性梳理」「高階」「結構性重組」「流程診斷師」「系統穩定器」這類顧問語言。
3. 不要捏造使用者沒有提到的成果、數據、職稱、專案名稱。
4. 如果使用者沒有明確提到衝突，不要直接寫「衝突調解」；可改成「溝通整理」「說法釐清」「責任釐清」。
5. 如果使用者沒有明確提到技術，不要把他寫成技術工程師。
6. 如果使用者沒有明確提到管理職，不要把他寫成主管或領導者。
7. 重點是隱性能力辨識，不是職涯配對。
8. 不要使用「你適合」「你應該」「最推薦你」這類語氣。
9. 多使用「可能」「比較像」「從你的描述看起來」這類語氣。

請固定輸出以下四段，不要增加第五段。
第一行必須直接從【1. 你不是在做雜事，而是在……】開始。
禁止輸出「First Voice 核心理解報告」「核心理解報告」「報告」或任何額外標題：

【1. 你不是在做雜事，而是在……】
請讓第一句獨立成為畫面焦點。
優先使用人話，不要使用顧問語言。

格式必須如下：

> 你不是在收拾雜事。  
> 你是在讓已經亂掉的事情，  
> 重新有辦法往前走。

可以依照使用者內容微調，但語氣要貼近真實工作現場。
不要使用「資訊流」「可執行的行動路徑」「行動路徑」「系統性梳理」「高階」「結構性重組」「流程診斷」這類顧問語言。
請優先使用「已經亂掉的事情」「大家不知道下一步」「重新往前走」「把說法整理清楚」「先知道可以往哪裡走」這類貼近真實工作現場的語言。

接著用 2 到 3 句說明：
- 使用者長期在處理什麼情境
- 做什麼判斷
- 補上什麼缺口
不要把第一段寫成報告摘要。

【2. 你的工作行為模式】
請根據初步分類與追問回答，說明使用者比較接近哪一種工作行為模式。
請使用「從你的描述看起來，你比較常被放在……的位置」這類語氣。
不要寫成「你就是某某類型的人」。
不要把它變成職稱推薦。
不要使用「流程診斷師」「系統穩定器」這類太像稱號的說法；請改用「常被放在釐清資訊、整理責任、拆出下一步的位置」。

【3. 你真正累積的隱性能力】
請把使用者的工作行為轉成能力語言。
請用 4 到 5 個短條列。
每一點格式必須如下：
- **能力名稱**：用 1 到 2 句說明這個能力實際上在做什麼。
每一點不要超過 70 字。
請依照使用者回答選擇，不要每次都列同一批能力。
可優先考慮這類較保守的能力名稱：
- 情境釐清能力
- 資訊整理能力
- 責任釐清能力
- 流程拆解能力
- 溝通整理能力
- 現場判斷能力
- 問題定位能力
- 執行銜接能力

【4. 為什麼這種能力常被低估】
請說明為什麼這類能力常被誤認為雜事、行政、救火、幫忙、補位。
重點是工作結構上的原因，不要寫成委屈抱怨。
請讓使用者理解：不是能力不存在，而是原本沒有被命名。
請使用這個方向：
「這類能力常常不容易被看見，因為它通常發生在問題被解決之前。」

最後加上這句，作為下一步提示：
「接下來，你可以選擇要把這段能力轉成哪一種用途：履歷、面試、作品集、社群貼文，或 AI 協作方式。」

以下是使用者資料：

使用者最近的困惑：
{original_concern}

入口題：
{entry_question}

使用者回答：
{entry_answer}

初步看到的工作模式：
{category_label}

分類說明：
{category_description}

判斷線索：
{category_reason}

追問 1：
{follow_q1}

使用者回答 1：
{follow_a1}

追問 2：
{follow_q2}

使用者回答 2：
{follow_a2}

請開始輸出四段核心結果。
"""


# ============================================================
# 用途轉譯 Prompt
# 第二層：使用者選擇一個用途後，才產出對應內容。
# ============================================================

USE_CASE_PROMPT_TEMPLATE = """
你是 First Voice 的第二層轉譯工具。

使用者已經完成核心理解：
他不是在做雜事，而是在把混亂轉換成別人可以前進的路。

現在請根據使用者選擇的用途，只輸出該用途需要的內容。
不要重複完整分析。
不要重新輸出核心結果。
不要同時輸出所有用途。
不要推薦職業。
不要捏造不存在的數據、職稱、專案名稱。

請使用繁體中文。
請使用台灣常用語氣。
請清楚、實用、可複製。
請避免空泛鼓勵。
請不要使用「你適合」「你應該」「最推薦你」。
請不要使用英文履歷模板句。

使用者選擇的用途：
{use_case}

使用者最近的困惑：
{original_concern}

入口題：
{entry_question}

使用者回答：
{entry_answer}

初步看到的工作模式：
{category_label}

分類說明：
{category_description}

判斷線索：
{category_reason}

追問 1：
{follow_q1}

使用者回答 1：
{follow_a1}

追問 2：
{follow_q2}

使用者回答 2：
{follow_a2}

請依照以下規則輸出：

如果用途是「履歷」：
標題用【履歷可用語句】
請提供 3 句履歷 bullet。
每句都要像履歷可以使用的語言。
不要捏造數據。
履歷句子要使用真實的人會用的語言。
不要使用「擔任樞紐」「主導制定」「具備...能力」「系統性地」「高度」「出色」這類抽象企業用語。
請改用：具體動詞 + 具體場景 + 實際作用。
例如：協助釐清跨部門流程中的資訊落差與責任歸屬，整理出後續可執行的處理步驟。
格式：
- ...
- ...
- ...

如果用途是「面試」：
標題用【面試可用說法】
請提供一段第一人稱說法。
語氣要像真實面試中可以講出來的內容。
請包含：
1. 我常被放在什麼情境
2. 我通常怎麼判斷
3. 我能帶來什麼具體作用
不要超過 180 字。

如果用途是「作品集」：
標題用【作品集可用描述】
請把這段經驗改寫成作品集 case study 的描述。
整段控制在 180 到 250 字。
「我的處理方式」最多 3 點，每點不超過 35 字。
不要寫成顧問報告。
格式：
- 情境：
- 問題：
- 我的處理方式：
  1. ...
  2. ...
  3. ...
- 產出或影響：
不要捏造數據。
不要自行加入「專案」「專案進度」「主管職」「管理成果」等使用者沒有明確提到的內容。
如果使用者只描述一般工作情境，請用「某件跨部門流程或客戶問題」這類保守說法。
請使用「協助釐清」「整理出下一步」「降低重複溝通」這類可信說法，避免「成功主導」「全面優化」。

如果用途是「社群貼文」：
標題用【社群貼文版本】
請各寫一版 LinkedIn 與 Threads。
兩版都必須使用繁體中文。
LinkedIn 版本：專業、清楚、適合放在職涯更新，控制在 120 字以內。
Threads 版本：比較口語、有現場感，但不要雞湯，不要可愛化，不要寫「小確幸」，控制在 120 字以內。
格式：
LinkedIn：
...

Threads：
...

如果用途是「AI 協作方式」：
標題用【你的個人 AI 協作方式】
這一段要假設使用者可能從來沒有用過 AI。
請固定包含以下五個小標：
這是什麼：
什麼時候可以用：
怎麼使用：
使用後會得到什麼：
可以帶到哪裡繼續用：

說明時請使用「工作經驗轉譯助手」或「工作行為分析助手」。
禁止使用「資深職涯顧問」「職涯教練」「獵頭顧問」。
不要寫「可量化的專業能力」。
請改成「更清楚、可被理解、可被使用的能力語言」。
請說明：First Voice 先在本地端用 Gemma 幫使用者建立工作語境；之後，使用者可以把這段完整語境帶到 Gemini、ChatGPT 或其他 AI 工具中繼續使用。
請不要把 Gemini 寫成主體，Gemini 只是後續協作工具之一。

接著提供一段可複製提示詞。
提示詞中的角色只能使用：
「你是一個工作經驗轉譯助手」
或
「你是一個工作行為分析助手」

提示詞要包含可填寫欄位：
【請貼上你的工作經驗】
【請選擇使用情境：履歷 / 面試 / 作品集 / LinkedIn / Threads / 其他】

如果用途是「快捷指令表」：
標題用【專屬快捷指令表】
請先說明：
這張表不是通用提示詞庫，而是使用者完成 First Voice 流程後，可以繼續和 AI 協作的延伸入口。
這些指令不是要單獨丟給 AI 使用，而是要搭配前面產出的工作模式、隱性能力與真實工作經驗，一起貼到 Gemini、ChatGPT 或其他 AI 工具中使用。

接著輸出「怎麼用」四步驟：
1. 先選你現在要完成的任務。
2. 複製右欄的 Prompt。
3. 把 First Voice 前面產出的工作模式與你的工作經驗一起貼進去。
4. 請 AI 依照你的用途繼續改寫。

然後請務必輸出標準 Markdown 表格。
表格前後都要空一行。
欄位固定為：
| 指令 | 適合什麼時候用 | 可複製 Prompt |
|---|---|---|

請產出 6 個指令，且只產出這 6 個：
/reframe
/resume
/interview
/portfolio
/linkedin
/promptme

每個可複製 Prompt 都要和使用者的工作行為模式有關。
每個 Prompt 請控制在 45 字以內，避免表格太長跑版。
"""


# ============================================================
# 文字清理
# 目的：
# 1. 避免模型偷渡不適合的語氣。
# 2. 避免作品滑向普通職涯推薦工具。
# 3. 保持台灣使用者較自然的語感。
# ============================================================

def clean_forbidden_words(text: str) -> str:
    replacements = {
        ("對" + "齊"): "整理成一致方向",
        ("共" + "情"): "理解",
        ("接" + "住"): "承接",
        ("對" + "接"): "銜接",
        "置關重要": "很重要",
        "賦能": "提供支援",
        "抓手": "切入點",
    }

    cleaned = text

    for bad_word, replacement in replacements.items():
        cleaned = cleaned.replace(bad_word, replacement)

    remove_phrases = [
        "好的，來幫你整理一下。",
        "好的，",
        "我來幫你整理一下。",
        "我來幫你",
        "以下是",
        "你適合",
        "你應該",
        "最推薦你",
        "非常適合你",
        "最適合你",
        "非常重要",
        "很棒",
        "很厲害",
        "小確幸",
        "天生就是",
        "命定",
        "完美符合",
        "人格特質測驗",
        "職涯方向推薦",
        "First Voice 核心理解報告",
        "核心理解報告",
        "資深職涯顧問",
        "職涯教練",
        "獵頭顧問",
        "可量化的專業能力",
        "擔任樞紐",
        "主導制定",
        "系統性地",
        "資訊流",
        "行動路徑",
        "可執行的行動路徑",
        "系統性梳理",
        "高階",
        "結構性重組",
        "流程診斷師",
        "系統穩定器",
        "MBTI",
        "星座",
    ]

    for phrase in remove_phrases:
        cleaned = cleaned.replace(phrase, "")

    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = cleaned.strip()

    return cleaned


# ============================================================
# 呼叫 Ollama
# ============================================================

def call_ollama(prompt: str, temperature: float = 0.2) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "top_p": 0.9,
            "repeat_penalty": 1.1
        }
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=180)
    response.raise_for_status()
    return response.json().get("response", "").strip()


# ============================================================
# JSON 解析
# ============================================================

def extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise ValueError("模型沒有回傳可讀取的 JSON。")


# ============================================================
# 備援分類器
# 模型無法穩定回傳時，仍讓 demo 可以跑。
# ============================================================

def fallback_classify(answer: str) -> str:
    text = answer.lower()

    keyword_map = {
        "stabilization": [
            "客訴", "危機", "爆炸", "吵架", "衝突", "突發", "緊急", "出事",
            "安撫", "抱怨", "現場失控", "很慌", "救火", "投訴", "失控"
        ],
        "technical": [
            "系統", "電腦", "網路", "設備", "技術", "錯誤", "bug", "資料",
            "工具", "程式", "當機", "表單", "軟體", "平台", "設定"
        ],
        "organization": [
            "文件", "流程", "整理", "表格", "紀錄", "排程", "分類", "規則",
            "資料夾", "行政", "會議紀錄", "一團亂", "混亂", "SOP", "清單"
        ],
        "mentoring": [
            "新人", "教", "帶人", "訓練", "說明", "教學", "實習生", "同事不會",
            "不懂流程", "陪", "引導", "示範"
        ],
        "coordination": [
            "溝通", "協作", "協調", "跨部門", "主管", "同事", "大家", "安排", "確認",
            "窗口", "卡住", "誰負責", "串", "聯絡", "通知"
        ],
    }

    scores = {key: 0 for key in CATEGORIES.keys()}

    for category, keywords in keyword_map.items():
        for word in keywords:
            if word in text:
                scores[category] += 1

    # 分類修正：
    # 若回答主要是「跨部門、誰負責、流程卡住、確認下一步」，
    # 即使出現客訴或抱怨，也優先視為 coordination。
    coordination_signals = [
        "跨部門", "誰負責", "下一步", "說法不同", "找誰確認",
        "流程卡住", "責任不清", "確認誰", "哪一段", "卡住"
    ]
    strong_stabilization_signals = [
        "失控", "情緒爆炸", "衝突升級", "現場壓不住",
        "緊急", "危機", "爆炸", "吵架"
    ]

    coordination_count = sum(1 for word in coordination_signals if word in text)
    strong_stabilization_count = sum(1 for word in strong_stabilization_signals if word in text)

    if coordination_count >= 2 and strong_stabilization_count == 0:
        return "coordination"

    best = max(scores, key=scores.get)

    if scores[best] == 0:
        return "organization"

    return best


# ============================================================
# 模型分類
# ============================================================

def classify_answer(original_concern: str, entry_answer: str) -> dict:
    user_prompt = f"""
以下是使用者目前的困惑：

{original_concern}

以下是使用者對入口題的回答：

入口題：{ENTRY_QUESTION}
回答：{entry_answer}

請判斷最接近的類型。
"""

    full_prompt = CLASSIFIER_PROMPT + "\n\n" + user_prompt

    try:
        raw = call_ollama(full_prompt, temperature=0.1)
        data = extract_json(raw)

        category = data.get("category", "").strip()
        reason = data.get("reason", "").strip()
        reason = clean_forbidden_words(reason)

        if category not in CATEGORIES:
            category = fallback_classify(entry_answer)
            reason = "模型判斷不夠明確，因此先依照回答中的工作線索做暫時分類。"

        return {
            "category": category,
            "reason": reason
        }

    except Exception:
        category = fallback_classify(entry_answer)
        return {
            "category": category,
            "reason": "模型暫時沒有穩定回覆，因此先用備援規則判斷。"
        }


# ============================================================
# 第一階段：分析工作行為模式，並產生追問
# ============================================================

def analyze_pattern(original_concern: str, entry_answer: str):
    if not original_concern.strip():
        return (
            "請先填寫你的工作、經驗或轉職困惑。",
            "",
            "",
            "",
            "",
            "",
            "",
        )

    if not entry_answer.strip():
        return (
            "請先回答入口題。",
            "",
            "",
            "",
            "",
            "",
            "",
        )

    result = classify_answer(original_concern, entry_answer)
    category = result["category"]
    reason = clean_forbidden_words(result["reason"])

    info = CATEGORIES[category]
    label = info["label"]
    description = info["description"]
    q1, q2 = info["questions"]

    pattern_text = f"""
從你的描述裡，有一件事慢慢浮現出來：

【{label}】

{description}

這不只是雜事，而是一種你反覆在工作中做的事。  
先不用急著把它變成職稱，我們先把它看清楚。

判斷線索：
{reason}
""".strip()

    pattern_text = clean_forbidden_words(pattern_text)

    return (
        pattern_text,
        q1,
        q2,
        category,
        reason,
        label,
        description,
    )


# ============================================================
# 第二階段：產出 First Voice 核心結果
# 只保留情緒峰值與核心理解，不一次塞入所有工具層。
# ============================================================

def generate_core_result(
    original_concern: str,
    entry_answer: str,
    follow_a1: str,
    follow_a2: str,
    category: str,
    category_reason: str,
    category_label: str,
    category_description: str,
):
    if not category:
        return "請先按上方的「分析我的工作模式」，產生初步模式與追問。"

    if not follow_a1.strip() or not follow_a2.strip():
        return "請先回答追問 1 和追問 2，再產出核心結果。"

    info = CATEGORIES.get(category, {})
    questions = info.get("questions", ["", ""])
    follow_q1 = questions[0]
    follow_q2 = questions[1]

    prompt = CORE_RESULT_PROMPT_TEMPLATE.format(
        original_concern=original_concern,
        entry_question=ENTRY_QUESTION,
        entry_answer=entry_answer,
        category_label=category_label,
        category_description=category_description,
        category_reason=category_reason,
        follow_q1=follow_q1,
        follow_a1=follow_a1,
        follow_q2=follow_q2,
        follow_a2=follow_a2,
    )

    try:
        result = call_ollama(prompt, temperature=0.3)
        return clean_forbidden_words(result)

    except Exception as e:
        return f"""
目前無法產出核心結果。

可能原因：
1. Ollama 沒有啟動。
2. 模型名稱不是 {OLLAMA_MODEL}。
3. 本機模型回應逾時。
4. 本機模型正在載入，請稍後重新執行一次。

技術訊息：
{str(e)}
""".strip()


# ============================================================
# 第三階段：依照使用者選擇，產出單一用途轉譯
# ============================================================

def fixed_shortcut_table() -> str:
    """固定產生快捷指令表，避免模型輸出表格不穩。"""
    return """
【專屬快捷指令表】

這張表不是通用提示詞庫。  
它是你完成 First Voice 之後，可以繼續和 AI 協作的延伸入口。

這些指令不是要單獨丟給 AI 使用。  
請搭配前面已經整理出的工作模式、隱性能力與真實工作經驗，一起貼到 Gemini、ChatGPT 或其他 AI 工具中使用。

怎麼用：
1. 先選你現在要完成的任務。
2. 複製右欄的 Prompt。
3. 把 First Voice 前面產出的工作模式與你的工作經驗一起貼進去。
4. 請 AI 依照你的用途繼續改寫。

| 指令 | 適合什麼時候用 | 可複製 Prompt |
|---|---|---|
| /reframe | 想重新理解工作經驗時 | 請根據我的工作經驗與 First Voice 產出的工作模式，重新整理我真正累積的能力。 |
| /resume | 要寫履歷時 | 請根據我的工作經驗與隱性能力，改寫成 3 句自然可信的履歷 bullet。 |
| /interview | 要準備面試時 | 請根據我的工作模式與經驗，整理成一段真實可說的面試回答。 |
| /portfolio | 要做作品集時 | 請根據我的工作經驗，整理成情境、問題、處理方式與影響。 |
| /linkedin | 要寫職涯貼文時 | 請根據我的工作模式，改寫成一篇自然、有現場感的 LinkedIn 貼文。 |
| /promptme | 不知道怎麼問 AI 時 | 請根據我的目標，幫我產生一段更清楚、可直接使用的 AI 指令。 |
""".strip()


def generate_use_case_result(
    use_case: str,
    original_concern: str,
    entry_answer: str,
    follow_a1: str,
    follow_a2: str,
    category: str,
    category_reason: str,
    category_label: str,
    category_description: str,
):
    if not category:
        return "請先完成上方的分析與核心結果，再選擇用途。"

    if not use_case:
        return "請先選擇你想轉成哪一種用途。"

    if use_case == "快捷指令表":
        return fixed_shortcut_table()

    info = CATEGORIES.get(category, {})
    questions = info.get("questions", ["", ""])
    follow_q1 = questions[0]
    follow_q2 = questions[1]

    prompt = USE_CASE_PROMPT_TEMPLATE.format(
        use_case=use_case,
        original_concern=original_concern,
        entry_question=ENTRY_QUESTION,
        entry_answer=entry_answer,
        category_label=category_label,
        category_description=category_description,
        category_reason=category_reason,
        follow_q1=follow_q1,
        follow_a1=follow_a1,
        follow_q2=follow_q2,
        follow_a2=follow_a2,
    )

    try:
        result = call_ollama(prompt, temperature=0.3)
        return clean_forbidden_words(result)

    except Exception as e:
        return f"""
目前無法產出用途版本。

可能原因：
1. Ollama 沒有啟動。
2. 模型名稱不是 {OLLAMA_MODEL}。
3. 本機模型回應逾時。
4. 本機模型正在載入，請稍後重新執行一次。

技術訊息：
{str(e)}
""".strip()


# ============================================================
# Gradio 介面
# ============================================================

with gr.Blocks(title=TITLE) as demo:
    category_state = gr.State("")
    reason_state = gr.State("")
    label_state = gr.State("")
    description_state = gr.State("")

    gr.Markdown(
        f"""
# {TITLE}

### {SUBTITLE}

如果，那些大家總是找你收拾的混亂，  
那些你默默讓事情重新動起來的瞬間，  
其實不是「雜事」，而是你最真實的能力？

First Voice 不是 AI 寫作工具，  
也不是職涯顧問或履歷生成器。

它從你真實的工作現場開始：

大家什麼時候會找你？  
你最常被找去處理哪一類卡住、混亂或說不清楚的事？  
你通常怎麼判斷，問題真正卡在哪裡？

> 你以為的雜事，  
> 可能是在把混亂轉換成別人可以前進的路。

全程在你自己的電腦裡完成。  
不上傳、不外流、不交給雲端。

請先從一段真實工作經驗開始。
"""
    )

    original_concern = gr.Textbox(
        label="請寫下你最近對工作、經驗或轉職的困惑",
        placeholder="例如：我做過很多不同工作，但不知道這些經驗能不能算成一種專長。",
        lines=4
    )

    entry_answer = gr.Textbox(
        label=ENTRY_QUESTION,
        placeholder="例如：大家常找我處理客戶抱怨、流程卡住、跨部門沒人知道誰負責的事。",
        lines=5
    )

    analyze_btn = gr.Button("幫我看見這段經驗")

    pattern_output = gr.Textbox(
        label="從你的描述裡，慢慢浮現的事情",
        lines=9
    )

    follow_q1 = gr.Textbox(
        label="追問 1",
        lines=2,
        interactive=False
    )

    follow_a1 = gr.Textbox(
        label="不用寫得正式，先描述你當時會怎麼做。",
        placeholder="照你平常處理事情的方式說就好，不用整理成標準答案。",
        lines=4
    )

    follow_q2 = gr.Textbox(
        label="追問 2",
        lines=2,
        interactive=False
    )

    follow_a2 = gr.Textbox(
        label="不用整理成標準答案，照你平常判斷的方式說就好。",
        placeholder="可以描述你會先看什麼、問誰、怎麼判斷下一步。",
        lines=4
    )

    final_btn = gr.Button("看看我一直在做什麼")

    final_output = gr.Markdown(
        label="先看見你一直在做的事"
    )

    gr.Markdown(
        """
---

### 下一步：把這段能力轉成你現在需要的用途

核心結果先停在「重新理解自己」。  
接下來，如果你想實際拿去用，再選一種用途產生即可。
"""
    )

    use_case = gr.Radio(
        choices=[
            "履歷",
            "面試",
            "作品集",
            "社群貼文",
            "AI 協作方式",
            "快捷指令表",
        ],
        label="你現在最想把這段能力用在哪裡？",
        value="履歷"
    )

    use_case_btn = gr.Button("產出這個用途的版本")

    use_case_output = gr.Markdown(
        label="用途轉譯結果"
    )

    analyze_btn.click(
        fn=analyze_pattern,
        inputs=[original_concern, entry_answer],
        outputs=[
            pattern_output,
            follow_q1,
            follow_q2,
            category_state,
            reason_state,
            label_state,
            description_state,
        ]
    )

    final_btn.click(
        fn=generate_core_result,
        inputs=[
            original_concern,
            entry_answer,
            follow_a1,
            follow_a2,
            category_state,
            reason_state,
            label_state,
            description_state,
        ],
        outputs=[final_output]
    )

    use_case_btn.click(
        fn=generate_use_case_result,
        inputs=[
            use_case,
            original_concern,
            entry_answer,
            follow_a1,
            follow_a2,
            category_state,
            reason_state,
            label_state,
            description_state,
        ],
        outputs=[use_case_output]
    )


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7861)
