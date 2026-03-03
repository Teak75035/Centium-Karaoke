import os
from mutagen.flac import FLAC

def krk_to_flac(tag_key="KRK_DATA"):
    for f in os.listdir("."):
        if not f.lower().endswith(".krk"):
            continue

        base = os.path.splitext(f)[0]
        flac_file = f"{base}.flac"
        if not os.path.exists(flac_file):
            print(f"跳过：无对应flac → {f}")
            continue

        try:
            with open(f, "r", encoding="utf-8") as fp:
                content = fp.read()
        except Exception as e:
            print(f"读取 {f} 失败：{e}")
            continue

        try:
            audio = FLAC(flac_file)
            audio[tag_key] = content
            audio.save()
            print(f"已写入：{f} → {flac_file}")
        except Exception as e:
            print(f"写入 {flac_file} 失败：{e}")

if __name__ == "__main__":
    krk_to_flac(tag_key="KRK_DATA")
