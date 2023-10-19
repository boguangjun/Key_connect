from flask import Flask, request, render_template
import pandas as pd
import base64


app = Flask(__name__)

# 假设这是您的后台数据，一个字典用于存储键值对


table_data = pd.read_excel("biao/yijibiao/your_table.csv")  # 请替换为您的表格文件

data = {
    "key1": "10",
    "key2": "15",
    "key3": "12"
}



def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
    return image_base64

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_data = request.form.get("input_data")
        result = table_data[table_data['Name'] == input_data]

        if not result.empty:
            name = result.iloc[0]['Name']
            image_path = result.iloc[0]['Data']

            # 构造图像文件的完整路径
            image_path = os.path.join("texture", image_path)

            # 将图像文件转换为base64编码的字符串
            data_base64 = image_to_base64(image_path)
        else:
            name = "未找到匹配值"
            data_base64 = ""

        return render_template("index.html", name=name, data_base64=data_base64, table_data1=table_data)  # 确保table_data变量被传递
    return render_template("index.html", name="", data_base64="", table_data1=table_data)  # 确保table_data变量被传递
def index1():
    if request.method == "POST1":
        input_data = request.form.get("input_data")
        result = data.get(input_data, "未找到匹配值")
        return render_template("index.html", result=result)
    return render_template("index.html", result="")

if __name__ == "__main__":
    webbrowser.open('http://localhost:3286/')
    app.run(host="localhost", port=3286)
