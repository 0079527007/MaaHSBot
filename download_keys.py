"""下载 OCR 模型的 keys.txt"""
import urllib.request
import os

dest = "sample/resource/model/ocr/keys.txt"

# 先试 GitHub raw
urls = [
    "https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.7/ppocr/utils/ppocr_keys_v1.txt",
    "https://huggingface.co/SWHL/RapidOCR/raw/main/PP-OCRv4/ppocr_keys_v1.txt",
]

for url in urls:
    try:
        print(f"尝试: {url}")
        urllib.request.urlretrieve(url, dest)
        size = os.path.getsize(dest) / 1024
        print(f"成功! 大小: {size:.1f} KB")
        break
    except Exception as e:
        print(f"失败: {e}")
else:
    print("所有源都失败!")
    # 最后手段：生成最小 keys.txt
    print("生成最小 keys.txt")
    # 添加常用中文OCR字符
    chars = []
    # 空格
    chars.append(" ")
    # 数字
    for c in "0123456789":
        chars.append(c)
    # 英文字母
    for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        chars.append(c)
    # 常用中文（炉石相关）
    for c in "开始匹配对战斗选狂野模式回合结束继续取消确认":
        chars.append(c)
    with open(dest, "w", encoding="utf-8") as f:
        f.write("\n".join(chars))
    print(f"生成最小 keys.txt ({len(chars)} 字符)")