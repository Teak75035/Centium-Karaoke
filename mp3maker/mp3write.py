import os
from mutagen.id3 import ID3, TXXX, ID3NoHeaderError

def write_krk_to_mp3(krk_key="krk_data"):
    """
    遍历当前目录，将xxx.krk内容写入xxx.mp3的TXXX:krk_data标签
    :param krk_key: TXXX标签的描述符，固定为krk_data
    """
    current_dir = os.getcwd()
    print(f"开始处理目录：{current_dir}\n")

    for filename in os.listdir(current_dir):
        # 仅处理.krk文件
        if not filename.lower().endswith(".krk"):
            continue
        
        krk_path = os.path.join(current_dir, filename)
        base_name = os.path.splitext(filename)[0]
        mp3_path = os.path.join(current_dir, f"{base_name}.mp3")

        # 检查对应MP3是否存在
        if not os.path.exists(mp3_path):
            print(f"❌ 跳过 {filename}：未找到同名MP3文件")
            continue

        # 读取KRK内容
        try:
            with open(krk_path, "r", encoding="utf-8") as f:
                krk_content = f.read().strip()
            if not krk_content:
                print(f"❌ 跳过 {filename}：KRK文件内容为空")
                continue
        except Exception as e:
            print(f"❌ 读取 {filename} 失败：{str(e)}")
            continue

        # 写入MP3的TXXX标签
        try:
            # 加载ID3标签，无标签则新建
            try:
                audio = ID3(mp3_path)
            except ID3NoHeaderError:
                audio = ID3()  # 新建ID3v2.3标签
            
            # 先删除旧标签，避免重复
            if krk_key in audio:
                del audio[krk_key]
            
            # 添加TXXX标签：UTF-8编码（encoding=3）
            audio.add(
                TXXX(
                    encoding=3,
                    desc=krk_key,
                    text=krk_content
                )
            )
            # 保存为ID3v2.3，兼容所有播放器
            audio.save(mp3_path, v2_version=3)
            print(f"✅ 成功写入：{mp3_path} <- {filename}")
        except Exception as e:
            print(f"❌ 写入 {mp3_path} 失败：{str(e)}")

    print("\n✅ 所有文件处理完成！")

if __name__ == "__main__":
    write_krk_to_mp3(krk_key="krk_data")
