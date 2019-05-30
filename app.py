#-*- coding:utf-8 -*-
from flask import Flask, abort, request, jsonify
import os
import ocr
import cv2
import bank_flow_gs_identity
app = Flask(__name__)

# 测试数据暂时存放
tasks = []


@app.route('/identify/text/', methods=['POST'])
def identify_text():
    if request.method == 'POST':
        f = request.files['file']
        # basepath = os.path.dirname(__file__)  # 当前文件所在路径
        # upload_path = os.path.join(basepath, 'static/uploads',f.filename)  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        upload_path = os.path.join(os.getcwd(), 'static/uploads/', f.filename)
        print(upload_path)
        f.save(upload_path)
        image = cv2.imread(upload_path, 1)
        #result=ocrText(upload_path)
        res=''
        result, image_framed = ocr.model(image)
        for key in result:
            print(result[key][1])
            res = res+(result[key][1])
        if (os.path.exists(upload_path)):
            os.remove(upload_path)
    return jsonify({'result': res})

@app.route('/identify/bank_flow/', methods=['POST'])
def bank_flow():
    if request.method == 'POST':
        f = request.files['file']
        #basepath = os.path.dirname(__file__)  # 当前文件所在路径
        #upload_path = os.path.join(basepath, 'static/uploads',f.filename)  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        upload_path=os.path.join(os.getcwd(), 'static/uploads/',f.filename)
        print(upload_path)
        f.save(upload_path)
        result=bank_flow_gs_identity.bank_flow_identity(upload_path)

        if (os.path.exists(upload_path)):
            os.remove(upload_path)
    return jsonify({'result': result})
if __name__ == "__main__":
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    app.run(host="0.0.0.0", port=8383, debug=False)
