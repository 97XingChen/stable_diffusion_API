from flask import Flask,render_template,request,jsonify,Response
import json,os,glob



app=Flask(__name__)
@app.route("/photo/<path:imageId>")
def get_frame(imageId):
    """
    :给图片制作接口，可以用url 返回图片jpg
    :param imageId:
    :return:resp
    """
    with open(r'/home/photo/{}'.format(imageId), 'rb') as f:
        image = f.read()
        resp = Response(image, mimetype="image/jpg")
        return resp
#

@app.route('/all_pthoto')
def get_date_pictures_path():
    """
    :param start_date和end_date 通过输入起始日期和结束日期选定需要用的日期
    :通过
    :return: Mark_dict_json
    """
    start_date=request.args.get('start_date')
    end_date = request.args.get('end_date')
    base_path = r'/home/photo'
    ##获取photo下的所有日期
    dirs_date=os.listdir(base_path)
    ##获取选中需要的日期
    return_date=[date  for  date in  dirs_date    if int(date)>=int(start_date) and  int(date)<=int(end_date)]
    ##列表存储数据
    Mark_dict_list=[]
    for  date in return_date:
        ##获取某日期下的所有图片的路径
        dir_path = f'{base_path}/{date}/**/*.*'
        phtots_path = glob.glob(dir_path, recursive=True)
        phtots_path =[ path.replace(base_path+'/','') for path in phtots_path]
        ##获取图片的标签
        for phtot_path  in phtots_path:
            Mark_dict={}
            Mark=phtot_path.split('/')
            Mark_dict['date']=Mark[0]
            Mark_dict['Category_zh'] = Mark[1]
            Mark_dict['Class_zh'] = Mark[2]
            Mark_dict['phtot_path'] = 'http://27.148.205.200:5000/photo/'+phtot_path
            Mark_dict_list.append(Mark_dict)
    Mark_dict_json=json.dumps(Mark_dict_list,ensure_ascii=False)
    return Mark_dict_json

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, debug=True)






