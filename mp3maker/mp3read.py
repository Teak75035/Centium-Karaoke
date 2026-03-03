import os
from mutagen.id3 import ID3, ID3NoHeaderError

def read_krk_from_mp3(krk_key="krk_data"):
    """
    遍历当前目录，从xxx.mp3的TXXX:krk_data提取内容，导出为xxx.krk
    :param krk_key: 要读取的TXXX标签描述符，需与写入时一致
    """
    current_dir = os.getcwd()
    print(f"开始处理目录：{current_dir}\n")

    for filename in os.listdir(current_dir):
        # 仅处理.mp3文件
        if not filename.lower().endswith(".mp3"):
            continue
        
        mp3_path = os.path.join(current_dir, filename)
        base_name = os.path.splitext(filename)[0]
        krk_path = os.path.join(current_dir, f"{base_name}.krk")

        # 读取MP3的ID3标签
        try:
            audio = ID3(mp3_path)
        except ID3NoHeaderError:
            print(f"❌ 跳过 {filename}：无ID3标签")
            continue
        except Exception as e:
            print(f"❌ 读取 {filename} 失败：{str(e)}")
            continue

        # 提取TXXX:krk_data内容
        try:
            # 从TXXX帧中筛选对应描述符的内容
            krk_frames = [f for f in audio.getall("TXXX") if f.desc == krk_key]
            if not krk_frames:
                print(f"❌ 跳过 {filename}：未找到TXXX:{krk_key}标签")
                continue
            
            # ✅ 核心修复：mutagen返回的text是列表，转成字符串（兼容单/多元素）
            krk_content = krk_frames[0].text
            if isinstance(krk_content, list):
                krk_content = "".join(krk_content)
            if not krk_content:
                print(f"❌ 跳过 {filename}：TXXX标签内容为空")
                continue
        except Exception as e:
            print(f"❌ 提取 {filename} 标签失败：{str(e)}")
            continue

        # 导出为.krk文件
        try:
            with open(krk_path, "w", encoding="utf-8") as f:
                f.write(krk_content)
            print(f"✅ 成功导出：{krk_path} <- {filename}")
        except Exception as e:
            print(f"❌ 写入 {krk_path} 失败：{str(e)}")

    print("\n✅ 所有文件处理完成！")

if __name__ == "__main__":
    read_krk_from_mp3(krk_key="krk_data")
