import os
import io
import uuid
import sys
import cv2
import base64
import logging
import numpy as np
from PIL import Image
from io import BytesIO
from flask import Flask, render_template, make_response, flash
import flask

#from flask_ngrok import run_with_ngrok #to run the application on colab using ngrok
import test_onnx

app = Flask(__name__)
# run_with_ngrok(app)


def convert_bytes_to_image(img_name,img_bytes):
    #将bytes结果转化为字节流
    bytes_stream = BytesIO(img_bytes)
    #读取到图片
    roiimg = Image.open(bytes_stream)
    img_path = os.path.join('./input', img_name + ".jpg")
    imgByteArr = BytesIO()    #初始化一个空字节流
    roiimg.save(imgByteArr,format('PNG'))     #把我们得图片以‘PNG’保存到空字节流
    imgByteArr = imgByteArr.getvalue()    #无视指针，获取全部内容，类型由io流变成bytes。
    with open(img_path,'wb') as f:
        f.write(imgByteArr)

    return img_path

@app.route('/')
@app.route('/api', methods=["POST", "GET"])
def api():
  try:
    img = flask.request.files["image"].read()
    img_name = str(uuid.uuid4())
    input_img_path = convert_bytes_to_image(img_name,img)
    output_img_path = os.path.join('./output', img_name + ".png")
    
    test_onnx.main(input_img_path,output_img_path)
    
    if os.path.exists(input_img_path):  # 如果文件存在
      os.remove(input_img_path)  
    else:
      logging.error('no such file')  # 则返回文件不存在
    try:
        with open(output_img_path, 'rb') as f:
          res = base64.b64encode(f.read())
        if os.path.exists(output_img_path):  # 如果文件存在
          os.remove(output_img_path)  
        else:
          logging.error('no such file')  # 则返回文件不存在
        return res
    except Exception as e:
        return "未识别到人脸"
  except Exception as e:
    print(e)
    return "errorError occurred, please check the log output！"


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 9000)))
    #app.run()
