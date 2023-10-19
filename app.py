from flask import Flask, request, render_template, redirect
import pandas as pd
import base64
import os
import webbrowser  
from werkzeug.utils import secure_filename  # 用于安全保存上传的文件
import random
import string



app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
app.config['UPLOAD_FOLDER'] = 'uploads'  # 存放上传文件的目录
app.config['TEXTURE_FOLDER'] = 'texture'  # 存放图片的目录

# 创建上传和图片保存的目录
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TEXTURE_FOLDER'], exist_ok=True)



table_data = pd.read_excel("biao/yijibiao/games.xlsx")  # 请替换为您的表格文件
key_data = pd.read_excel("biao/yijibiao/key.xlsx")
chengyuan_data = pd.read_excel("biao/yijibiao/chengyuan.xlsx")
used_key = pd.DataFrame(columns=['兑换码编号', '兑换码', '游戏', '是否被领取', '领取人', '领取人是否给出评测',"steam评测地址"])
waiting_key = pd.DataFrame(columns=['兑换码编号', '兑换码', '游戏', '是否被领取', '领取人', '领取人是否给出评测',"steam评测地址"])
fresh_key = pd.DataFrame(columns=['兑换码编号', '兑换码', '游戏', '是否被领取', '领取人', '领取人是否给出评测',"steam评测地址"])
key_ap = pd.DataFrame(columns=['兑换码编号', '兑换码', '游戏', '是否被领取', '领取人', '领取人是否给出评测',"steam评测地址"])
deleted_games = pd.DataFrame(columns=table_data.columns)





##定义一下刷新用的函数

###刷新key的表格
def RG_key_xls():###重新载入已经编辑完成的游戏兑换密匙表格
    global key_dataI
    key_dataI = pd.read_excel("biao/yijibiao/key.xlsx")
    print(key_data)
    global used_keyI
    global waiting_keyI
    global fresh_keyI
    used_keyI = pd.DataFrame(columns=['兑换码编号', '兑换码', '游戏', '是否被领取', '领取人', '领取人是否给出评测',"steam评测地址"])
    waiting_keyI = pd.DataFrame(columns=['兑换码编号', '兑换码', '游戏', '是否被领取', '领取人', '领取人是否给出评测',"steam评测地址"])
    fresh_keyI = pd.DataFrame(columns=['兑换码编号', '兑换码', '游戏', '是否被领取', '领取人', '领取人是否给出评测',"steam评测地址"])
    #重置完成，开始重新载入各个表格信息
    for index0, row in key_dataI.iterrows():

        dhmH = row['兑换码编号']
        dhm = row['兑换码']
        game = row['游戏']
        get = row['是否被领取']
        getM =row['领取人']
        PC = row['领取人是否给出评测']
        PCS = row['steam评测地址']
        if get == "是":##是否已经被领取
            new_row_uk = {'兑换码编号':dhmH,'兑换码':dhm,'游戏':game,'是否被领取':get,'领取人':getM,'领取人是否给出评测':PC,'steam评测地址':PCS}
            used_keyI = used_keyI.append(new_row_uk, ignore_index=True)
            if PC == '否':
                new_row_wk = {'兑换码编号':dhmH,'兑换码':dhm,'游戏':game,'是否被领取':get,'领取人':getM,'领取人是否给出评测':PC,'steam评测地址':PCS}
                waiting_keyI = waiting_keyI.append(new_row_wk, ignore_index=True)
        if get == '否':###还没有被领取的
            new_row_fk = {'兑换码编号':dhmH,'兑换码':dhm,'游戏':game,'是否被领取':get,'领取人':getM,'领取人是否给出评测':PC,'steam评测地址':PCS}
            fresh_keyI = fresh_keyI.append(new_row_fk, ignore_index=True)
##刷新key的表格完成


##刷新每个人的的领到手的key
def RG_key_lqr(lingquren):###重新载入已经编辑完成的游戏兑换密匙表格
    global key_apI
    key_apI = pd.DataFrame(columns=['兑换码编号', '兑换码', '游戏', '是否被领取', '领取人', '领取人是否给出评测',"steam评测地址"])
    for index1, row in key_data.iterrows():
        dhmH = row['兑换码编号']
        dhm = row['兑换码']
        game = row['游戏']
        get = row['是否被领取']
        getM =row['领取人']
        PC = row['领取人是否给出评测']
        PCS = row['steam评测地址']
        if row['领取人'] == lingquren:
            new_row_api = {'兑换码编号':dhmH,'兑换码':dhm,'游戏':game,'是否被领取':get,'领取人':getM,'领取人是否给出评测':PC,'steam评测地址':PCS}
            key_apI = key_apI.append(new_row_api, ignore_index=True)
##刷新每个人的的领到手的key


###刷新每个游戏的key
def RG_key_gam(game_name_in):###重新载入已经编辑完成的游戏兑换密匙表格
    global key_gameI
    key_gameI = pd.DataFrame(columns=['兑换码编号', '兑换码', '游戏', '是否被领取', '领取人', '领取人是否给出评测',"steam评测地址"])
    for index2, row in key_data.iterrows():
        dhmH = row['兑换码编号']
        dhm = row['兑换码']
        game = row['游戏']
        get = row['是否被领取']
        getM =row['领取人']
        PC = row['领取人是否给出评测']
        PCS = row['steam评测地址']
        if row['游戏'] == game_name_in:
            new_row_gameI = {'兑换码编号':dhmH,'兑换码':dhm,'游戏':game,'是否被领取':get,'领取人':getM,'领取人是否给出评测':PC,'steam评测地址':PCS}
            key_gameI = key_gameI.append(new_row_gameI, ignore_index=True)
###刷新每个游戏的key
















###下面是一个刷新key的例子，在对key修改之后一定要记得刷新一下
RG_key_xls()
key_data = key_dataI.copy()
used_key = used_keyI.copy()
waiting_key = waiting_keyI.copy()
fresh_key = fresh_keyI.copy()
###上面是一个刷新key的例子，在对key修改之后一定要记得刷新一下

###下面是一个刷新每个人领取的key的例子，在对key修改之后一定要记得刷新一下
RG_key_lqr("伯辉")
#key_ap = key_apI.copy()
#print("伯辉的key有")
print(key_apI)
###上面是一个刷新key的例子，在对key修改之后一定要记得刷新一下














##下面开始定义的是当网页给予反馈的时候，给出的动作

@app.route("/details/<item_name>", methods=["GET"])
def show_item_details(item_name):
    # 在这里，item_name 是被点击的项目的名称
    # 你可以从 table_data 中查找该项目的详细信息，包括名称和图像
    print(item_name)
    result = table_data[table_data['Name'] == item_name]


    if not result.empty:
        name = result.iloc[0]['Name']
        image_path = result.iloc[0]['Data']

        # 将图像文件转换为base64编码的字符串
        image_path = os.path.join(image_path)
        print(image_path)
        data_base64 = image_to_base64(image_path)
    else:
        name = "未找到匹配值"
        data_base64 = ""
    RG_key_gam(item_name)
    return render_template("item_details.html", name=name, data_base64=data_base64,key_gameI=key_gameI)


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_path = os.path.join(image_path)
        print(image_path)
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
    return image_base64
app.jinja_env.globals.update(image_to_base64=image_to_base64)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_data = request.form.get("input_data")
        result = table_data[table_data['Name'] == input_data]

        if not result.empty:
            name = result.iloc[0]['Name']
            lianxiduixiang = result.iloc[0]['联系对象']
            lianxifangshi = result.iloc[0]['联系方式']
            beizhu = result.iloc[0]['备注']
            image_path = result.iloc[0]['Data']

            # 构造图像文件的完整路径
            print(image_path)
            image_path = os.path.join("texture", image_path)
            print(image_path)

            # 将图像文件转换为base64编码的字符串
            data_base64 = image_to_base64(image_path)
        else:
            name = "未找到匹配值"
            data_base64 = ""
        return render_template("index.html", name=name, data_base64=data_base64, table_data=table_data, image_to_base64=image_to_base64,lianxiduixiang = lianxiduixiang,lianxifangshi = lianxifangshi,beizhu = beizhu)
    return render_template("index.html", name="", data_base64="", table_data=table_data, image_to_base64=image_to_base64)



@app.route("/add_data", methods=["GET", "POST"])
def add_data():
    global table_data  # 将table_data声明为全局变量
    global key_data
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        contact = request.form.get("contact")
        phone = request.form.get("phone")
        image = request.files["image"]

        if name and description and contact and phone and image:
            # 生成一个随机的文件名
            random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.png'
            image.save(os.path.join(app.config['TEXTURE_FOLDER'], random_filename))
            file_place = 'texture/' + random_filename

            # 将数据添加到表格
            new_data = {
                'Name': name,
                'Data': file_place,
                '备注': description,
                '联系对象': contact,
                '联系方式': phone,
            }
            table_data = table_data.append(new_data, ignore_index=True)
            # 保存更新后的表格
            table_data.to_excel("biao/yijibiao/games.xlsx", index=False)

            return redirect('/')  # 重定向到首页或其他页面
        else:
            flash("请填写所有字段并上传图片")

    return render_template("add_data.html")



###确认是否删除游戏
@app.route('/delete_game_data_confirm/<delete_game_name>',methods=['GET','POST'])
def delete_game_data_confirm(delete_game_name):
    print(delete_game_name)
    return render_template('confirm_de.html',delete_game_name1=delete_game_name)





#删除游戏
@app.route('/delete_game_data/<game_name>',methods=['GET'])
def delete_game_data(game_name):
    global table_data
    global deleted_games
    print(game_name)
    # 检查数据框中是否存在特定名称的行
    if game_name in table_data['Name'].values:
        # 使用 drop 方法删除匹配的行
        deleted_row = table_data[table_data['Name'] == game_name].iloc[0]  # 提取被删除的行
        table_data = table_data[table_data['Name'] != game_name]
        deleted_games = deleted_games.append(deleted_row, ignore_index=True)  # 添加已删除的行到新数据框
        print(table_data)
        table_data.to_excel("biao/yijibiao/games.xlsx", index=False)
        deleted_games.to_excel("biao/yijibiao/deleted_games.xlsx", index=False)  # 保存已删除的行到另一个文件
        return redirect('/')
    else:
        return f'未找到游戏名为 {game_name} 的行'
        return redirect('/')



###下面是打开兑换码详情界面
@app.route("/duihuanmaxiangqing/<duihuanma_name>", methods=["GET","POST"])
def show_duihuanmaxiangqing(duihuanma_name):
    # 在这里，item_name 是被点击的项目的名称
    # 你可以从 table_data 中查找该项目的详细信息，包括名称和图像
    if request.method == "GET":
        result1 = key_data[key_data['兑换码编号'] == duihuanma_name]
        if not result1.empty:
            print("测试分歧1成立")
            duihuanmahao = result1.iloc[0]['兑换码编号']
            duihuanma = result1.iloc[0]['兑换码']
            youxi = result1.iloc[0]['游戏']
            shifoulingqu = result1.iloc[0]['是否被领取']
            lingquren = result1.iloc[0]['领取人']
            pingce = result1.iloc[0]['领取人是否给出评测']
            pingcewz = result1.iloc[0]['steam评测地址']
        else:
            name = "未找到匹配值"
        return render_template("show_key.html",pingcewz=pingcewz,pingce=pingce,lingquren=lingquren,youxi=youxi,shifoulingqu=shifoulingqu,duihuanmahao=duihuanmahao,duihuanma=duihuanma, )
    return render_template("show_key.html",pingcewz='',pingce='',lingquren='',youxi='',shifoulingqu='',duihuanmahao='',duihuanma='', )



###下面是进行兑换码状态变更界面
@app.route("/duihuanzhuangtaibiangeng/<duihuanma_name>", methods=["GET","POST"])
def duihuanzhuangtaibiangeng(duihuanma_name):
    global chengyuan_data
    if request.method == "GET": 
        result1 = key_data[key_data['兑换码编号'] == duihuanma_name]
        print(result1)
        if not result1.empty:
            duihuanmahao = result1.iloc[0]['兑换码编号']
            duihuanma = result1.iloc[0]['兑换码']
            youxi = result1.iloc[0]['游戏']
            shifoulingqu = result1.iloc[0]['是否被领取']
            lingquren = result1.iloc[0]['领取人']
            pingce = result1.iloc[0]['领取人是否给出评测']
            pingcewz = result1.iloc[0]['steam评测地址']
        else:
            name = "未找到匹配值"
        return render_template("add_key_data.html",pingcewz=pingcewz,pingce=pingce,lingquren=lingquren,youxi=youxi,shifoulingqu=shifoulingqu,duihuanmahao=duihuanmahao,duihuanma=duihuanma,char_list=chengyuan_data )

##变更完成

@app.route('/duihuanmabiangeng', methods=['GET', 'POST'])
def handle_form_submission():
    global key_data
    if request.method == 'POST':
        duihuanmahao = request.form['duihuanmahao']
        duihuanma = request.form['duihuanma']
        youxi = request.form['youxi']
        shifoulingqu = request.form['shifoulingqu']
        lingquren = request.form['lingquren']
        pingce = request.form['pingce']
        pingcewz = request.form['pingcewz']
        # 找到匹配的行
        matching_rows = key_data[key_data['兑换码编号'] == duihuanmahao]
        matching_row_indices = matching_rows.index[0]
        print(duihuanmahao)
        print(duihuanmahao)
        print("开始打印行号")
        print(matching_row_indices)

        if not matching_rows.empty:
            # 更新匹配的行
            key_data.at[matching_row_indices, '兑换码编号'] = duihuanmahao
            key_data.at[matching_row_indices, '兑换码'] = duihuanma
            key_data.at[matching_row_indices, '游戏'] = youxi
            key_data.at[matching_row_indices, '是否被领取'] = shifoulingqu
            key_data.at[matching_row_indices, '领取人'] = lingquren
            key_data.at[matching_row_indices, '领取人是否给出评测'] = pingce
            key_data.at[matching_row_indices, 'steam评测地址'] = pingcewz

            # 保存到Excel文件
            key_data.to_excel("biao/yijibiao/key.xlsx", index=False)
    return render_template('show_key.html', duihuanmahao=duihuanmahao, duihuanma=duihuanma, youxi=youxi, shifoulingqu=shifoulingqu, lingquren=lingquren, pingce=pingce, pingcewz=pingcewz)


###对每一个游戏添加key
@app.route('/add_keys_confirm/<gamename>', methods=['GET', 'POST'])
def add_keys_confirm(gamename):
    print(gamename)
    global key_data
    global chengyuan_data
    if request.method == "GET": 
        game_add_key = gamename
        shifoulingqu = "否"
        lingquren = ""
        pc = "否"
        pcdizhi = ""
        random_keybianhao = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return render_template("add_keys.html",keybianhao=random_keybianhao,game_add_key=game_add_key,shifoulingqu=shifoulingqu,lingquren=lingquren,pc=pc,pcdizhi=pcdizhi,char_list=chengyuan_data)

@app.route('/add_keys_submit', methods=['GET', 'POST'])
def add_keys_submit():
    global key_data
    print(request.method)
    if request.method == 'POST':
        print(request)
        print("回复打印完成")
        keybianhao = request.form.get('keybianhao')
        game_add_key = request.form.get('game_add_key')
        game_add_key = request.form.get('game_add_key')
        shifoulingqu = request.form.get('shifoulingqu')
        lingquren = request.form.get('lingquren')
        pc = request.form.get('pc')
        pingcewz = request.form.get('pingcewz')
        key = request.form.get('key')
        print(key)
        new_data1 = {
            '兑换码编号': keybianhao,
            '兑换码': key,
            '游戏': game_add_key,
            '是否被领取': shifoulingqu,
            '领取人': lingquren,
            '领取人是否给出评测': pc,
            'steam评测地址': pingcewz,
        }
        key_data = key_data.append(new_data1, ignore_index=True)
        # 保存更新后的表格
        key_data.to_excel("biao/yijibiao/key.xlsx", index=False)
        result20 = table_data[table_data['Name'] == game_add_key]

        if not result20.empty:
            name = result20.iloc[0]['Name']
            image_path = result20.iloc[0]['Data']

            # 将图像文件转换为base64编码的字符串
            image_path20 = os.path.join(image_path)
            print(image_path)
            data_base641 = image_to_base64(image_path20)
        else:
            name = "未找到匹配值"
            data_base64 = ""
        RG_key_gam(game_add_key)
        return render_template("item_details.html", name=name, data_base64=data_base641,key_gameI=key_gameI)


####然后是遍历每一个kay，然后把每一个key加载进一个列表
@app.route('/key_page', methods=['GET', 'POST'])
def keypage_show():
    return render_template("key_main_page.html",key_data=key_data)



####然后是遍历每一个kay，然后把每一个freshkey加载进一个列表
@app.route('/key_page_fresh', methods=['GET', 'POST'])
def keypage_show_f():
    RG_key_xls()
    key_fresh = fresh_keyI
    return render_template("key_main_page.html",key_data=key_fresh)

####然后是遍历每一个kay，然后把每一个freshkey加载进一个列表
@app.route('/key_page_waitting', methods=['GET', 'POST'])
def keypage_show_w():
    RG_key_xls()
    key_wait = waiting_keyI
    return render_template("key_main_page.html",key_data=key_wait)



###载入所有成员列表
@app.route('/chengyuan_list', methods=['GET', 'POST'])
def get_chengyuan_list():
    global chengyuan_data
    chengyuandata = chengyuan_data
    return render_template("chengyuanlist.html",chengyuan_data=chengyuan_data)


###载入成员信息表
@app.route('/chengyuan_xinxi/<chengyuanid>', methods=['GET', 'POST'])
def get_chengyuan_xinxi(chengyuanid):
    print(chengyuanid)
    global chengyuan_data
    result30 = chengyuan_data[chengyuan_data['id'] == chengyuanid]
    if not result30.empty:
        c_id = result30.iloc[0]['id']
        image_path = result30.iloc[0]['头像']
        qqhao = result30.iloc[0]['qq号']
        email = result30.iloc[0]['邮箱']
        tel = result30.iloc[0]['电话号码']
        other = result30.iloc[0]['其他联系方式']
        # 将图像文件转换为base64编码的字符串
        image_path = os.path.join(image_path)
        data_base643 = image_to_base64(image_path)
    else:
        name = "未找到匹配值"
        data_base64 = ""
    RG_key_lqr(chengyuanid)
    return render_template("chengyuanxinxi.html", chengyuanid=chengyuanid, data_base64=data_base643,qqhao=qqhao,email=email,tel=tel,other=other,key_apI=key_apI)

###添加成员进表
@app.route("/add_chengyuan", methods=["GET", "POST"])
def add_chengyuan():
    return render_template("chengyuantianjia.html")












###添加成员进表
@app.route("/add_chengyuan_xls", methods=["GET", "POST"])
def add_chengyuan_xls():
    global chengyuan_data  # 将table_data声明为全局变量
    if request.method == "POST":
        c_id = request.form.get("c_id")
        qq = request.form.get("qq")
        email = request.form.get("email")
        tel = request.form.get("tel")
        oth = request.form.get("oth")
        image = request.files["image"]


        if c_id and image:
            # 生成一个随机的文件名
            random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.png'
            image.save(os.path.join(app.config['TEXTURE_FOLDER'], random_filename))
            file_place = 'texture/' + random_filename

            # 将数据添加到表格
            new_data11 = {
                'id': c_id,
                '头像': file_place,
                'qq号': qq,
                '邮箱': email,
                '电话号码': tel,
                '其他联系方式': oth,
            }
            chengyuan_data = chengyuan_data.append(new_data11, ignore_index=True)
            # 保存更新后的表格
            chengyuan_data.to_excel("biao/yijibiao/chengyuan.xlsx", index=False)

            return redirect('/chengyuan_list')  # 重定向到首页或其他页面
        else:
            flash("请填写idb并上传头像")

    return render_template("chengyuantianjia.html")



#####下面变更成员信息：
@app.route("/change_chengyuan/<chengyuan_name>", methods=["GET","POST"])
def changyuan_change(chengyuan_name):
    global chengyuan_data
    global shabibianliang_quanjuchengyuantupian
    if request.method == "GET": 
        result40 = chengyuan_data[chengyuan_data['id'] == chengyuan_name]
        print(result40)
        if not result40.empty:
            c_id = result40.iloc[0]['id']
            touxiang = result40.iloc[0]['头像']
            qq = result40.iloc[0]['qq号']
            email = result40.iloc[0]['邮箱']
            tel = result40.iloc[0]['电话号码']
            oth = result40.iloc[0]['其他联系方式']
            image_path = os.path.join(touxiang)
            data_base644 = image_to_base64(image_path)
            shabibianliang_quanjuchengyuantupian = image_path
        else:
            c_id = "未找到匹配值"
        return render_template("chengyuangenggai.html",c_id=c_id,qq=qq,touxiang=data_base644,email=email,tel=tel,oth=oth)

##变更完成

@app.route('/change_chengyuan_ok', methods=['GET', 'POST'])
def changyuan_change_ok():
    global chengyuan_data
    global shabibianliang_quanjuchengyuantupian
    if request.method == 'POST':
        c_id = request.form['c_id']
        qq = request.form['qq']
        email = request.form['email']
        tel = request.form['tel']
        oth = request.form['oth']
        image = request.files["image"]
        if image:
            # 生成一个随机的文件名
            random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.png'
            image.save(os.path.join(app.config['TEXTURE_FOLDER'], random_filename))
            file_place = 'texture/' + random_filename
        else:
            file_place = shabibianliang_quanjuchengyuantupian
        # 找到匹配的行
        matching_rows = chengyuan_data[chengyuan_data['id'] == c_id]
        matching_row_indices = matching_rows.index[0]
        print("开始打印行号")
        print(matching_row_indices)

        if not matching_rows.empty:
            # 更新匹配的行
            chengyuan_data.at[matching_row_indices, 'id'] = c_id
            chengyuan_data.at[matching_row_indices, '头像'] = file_place
            chengyuan_data.at[matching_row_indices, 'qq号'] = qq
            chengyuan_data.at[matching_row_indices, '邮箱'] = email
            chengyuan_data.at[matching_row_indices, '电话号码'] = tel
            chengyuan_data.at[matching_row_indices, '其他联系方式'] = oth

            # 保存到Excel文件
            chengyuan_data.to_excel("biao/yijibiao/chengyuan.xlsx", index=False)

    RG_key_lqr(c_id)
    return render_template("chengyuanxinxi.html", chengyuanid=c_id, data_base64=image,qqhao=qq,email=email,tel=tel,other=oth,key_apI=key_apI)


#####下面变更游戏信息：
@app.route("/change_game_data/<game_name>", methods=["GET","POST"])
def game_change(game_name):
    print("收到游戏信息")
    print(game_name)
    global table_data
    global shabibianliang_quanjuyouxitupian
    if request.method == "GET": 
        result50 = table_data[table_data['Name'] == game_name]
        print(result50)
        if not result50.empty:
            name = result50.iloc[0]['Name']
            tupian = result50.iloc[0]['Data']
            lianxiduixiang = result50.iloc[0]['联系对象']
            lianxifangshi = result50.iloc[0]['联系方式']
            beizhu = result50.iloc[0]['备注']
            image_path = os.path.join(tupian)
            data_base646 = image_to_base64(image_path)
            shabibianliang_quanjuyouxitupian = image_path
        else:
            name = "未找到匹配值"
        return render_template("change_game_data.html",name=name,lianxiduixiang=lianxiduixiang,tupian=data_base646,lianxifangshi=lianxifangshi,beizhu=beizhu)

@app.route('/change_game_ok', methods=['GET', 'POST'])
def game_change_ok():
    global table_data
    global shabibianliang_quanjuyouxitupian
    if request.method == 'POST':
        name = request.form['name']
        lianxiduixiang = request.form['lianxiduixiang']
        lianxifangshi = request.form['lianxifangshi']
        beizhu = request.form['beizhu']
        image = request.files["image"]
        if image:
            # 生成一个随机的文件名
            random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.png'
            image.save(os.path.join(app.config['TEXTURE_FOLDER'], random_filename))
            file_place = 'texture/' + random_filename
        else:
            file_place = shabibianliang_quanjuyouxitupian
        # 找到匹配的行
        matching_rows = table_data[table_data['Name'] == name]
        matching_row_indices = matching_rows.index[0]

        if not matching_rows.empty:
            # 更新匹配的行
            table_data.at[matching_row_indices, 'Name'] = name
            table_data.at[matching_row_indices, 'Data'] = file_place
            table_data.at[matching_row_indices, '联系对象'] = lianxiduixiang
            table_data.at[matching_row_indices, '联系方式'] = lianxifangshi
            table_data.at[matching_row_indices, '备注'] = beizhu

            # 保存到Excel文件
            table_data.to_excel("biao/yijibiao/games.xlsx", index=False)

        file_place = os.path.join(file_place)
        print(file_place)
        data_base648 = image_to_base64(file_place)



        RG_key_gam(name)
        return render_template("item_details.html", name=name, data_base64=data_base648,key_gameI=key_gameI)



























if __name__ == "__main__":
    webbrowser.open('http://localhost:3286/')
    app.run(host="localhost", port=3286)