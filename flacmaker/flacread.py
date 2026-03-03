import os
from mutagen.flac import FLAC

def flac_to_krk(tag_key="KRK_DATA"):
    for f in os.listdir("."):
        if not f.lower().endswith(".flac"):
            continue

        base = os.path.splitext(f)[0]
        krk_file = f"{base}.krk"

        try:
            audio = FLAC(f)
        except Exception as e:
            print(f"{f} 读取失败：{e}")
            continue

        if tag_key not in audio:
            print(f"[{f}] 无 {tag_key} 标签")
            continue

        try:
            content = audio[tag_key][0]
            with open(krk_file, "w", encoding="utf-8") as fp:
                fp.write(content)
            print(f"导出成功：{krk_file}")
        except Exception as e:
            print(f"导出 {krk_file} 失败：{e}")

if __name__ == "__main__":
    flac_to_krk(tag_key="KRK_DATA")
