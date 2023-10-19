import pandas as pd
import os

# 初始化变量
huizongshurutishitianjia = ""
huizongzhilingyouxiaoxingjihuo = ""

# 读取 xlsx 表格
def read_excel_file(file_path):
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print("读取表格时出错:", e)
        return None

# 生成需要写入的文本内容
def generate_text_content(data_frame):
    shurutishitianjia = ""
    zhilingyouxiaoxingjihuo = ""
    for index, row in data_frame.iterrows():
        minglingneirong = row["命令内容"]
        zhiling = row["指令"]
        minglingwenjian = row["命令文件"]
        minglingwenjian2 = row["命令文件2"]
        minglingwenjian3 = row["命令文件3"]
        minglingwenjian4 = row["命令文件4"]
        minglingwenjian5 = row["命令文件5"]
        shurutishitianjia += f'echo "{minglingneirong}"的指令是"{zhiling}"\n'
        if minglingwenjian2 == "None":
            minglingwenjian2 = "tools\kong1.py"
        if minglingwenjian3 == "None":
            minglingwenjian3 = "tools\kong2.py"
        if minglingwenjian4 == "None":
            minglingwenjian4 = "tools\kong3.py"
        if minglingwenjian5 == "None":
            minglingwenjian5 = "tools\kong4.py"
        print(minglingwenjian)
        print(minglingwenjian2)
        print(minglingwenjian3)
        print(minglingwenjian4) 
        print(minglingwenjian5)      
        zhilingyouxiaoxingjihuo += (
            f') else if "%input%"=="{zhiling}" (\n'
            f'  set python_script={minglingwenjian}\n'
            f'  set python_script2={minglingwenjian2}\n'
            f'  set python_script3={minglingwenjian3}\n'
            f'  set python_script4={minglingwenjian4}\n'
            f'  set python_script5={minglingwenjian5}\n'
        )
    return shurutishitianjia, zhilingyouxiaoxingjihuo

# 保存文本内容到文件
def save_text_to_file(text_content, file_path):
    try:
        with open(file_path, "w", encoding="ansi") as file:
            file.write(text_content)
        print("文本保存成功")
    except Exception as e:
        print("保存文本时出错:", e)

def main():
    input_file = "biao/yijibiao/command_config.xlsx"  # 替换为实际的表格文件路径
    shurutishitianjia_output_file = "shurutishitianjia.txt"  # 替换为实际的输出文件路径
    zhilingyouxiaoxingjihuo_output_file = "zhilingyouxiaoxingjihuo.txt"  # 替换为实际的输出文件路径

    # 读取表格
    df = read_excel_file(input_file)
    if df is not None:
        # 生成文本内容
        shurutishitianjia, zhilingyouxiaoxingjihuo = generate_text_content(df)
        # 保存文本内容到文件
        save_text_to_file(shurutishitianjia, shurutishitianjia_output_file)
        save_text_to_file(zhilingyouxiaoxingjihuo, zhilingyouxiaoxingjihuo_output_file)
        # 更新 BAT 文件内容
        create_new_bat()

def create_new_bat():
    new_bat_content = []
    
    # 读取模板 BAT 文件内容
    with open("model.bat", "r") as model_bat_file:
        template_bat_content = model_bat_file.readlines()

    # 添加新的命令配置
    for line in template_bat_content:
        new_bat_content.append(line)
        if line.strip() == "echo 可执行的法术列表：":
            new_bat_content.append("\nREM 添加新命令\n")
            with open("shurutishitianjia.txt", "r") as shurutishitianjia_file:
                new_bat_content.extend(shurutishitianjia_file.readlines())
        if line.strip() == "set python_script=tools\kongg.py":
            new_bat_content.append("\nREM 添加新命令\n")
            with open("zhilingyouxiaoxingjihuo.txt", "r") as zhilingyouxiaoxingjihuo_file:
                new_bat_content.extend(zhilingyouxiaoxingjihuo_file.readlines())

    # 创建新的 BAT 文件
    with open("daobiao.bat", "w") as new_bat_file:
        new_bat_file.writelines(new_bat_content)

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"{file_path} 文件删除成功")
    except Exception as e:
        print(f"删除 {file_path} 文件时出错:", e)


if __name__ == "__main__":
    main()
    file_path = "shurutishitianjia.txt"  # 替换为实际的文件路径
    delete_file(file_path)
    file_path = "zhilingyouxiaoxingjihuo.txt"  # 替换为实际的文件路径
    delete_file(file_path)
