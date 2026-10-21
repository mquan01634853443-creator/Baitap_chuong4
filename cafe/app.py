from datetime import datetime
from flask import Flask, abort, render_template, request
app=Flask(__name__)
SHOP={"name":"Cà phê Sông Hương","address":"12 Lê Lợi, Huế","phone":"0234 3888 999","open":7,"close":22}
PROMOTIONS=["Giảm 10% cho sinh viên","Mua 2 tặng 1 vào thứ hai"]
MENU=[
{"id":1,"name":"Cà phê đen","price":20000,"available":True,"image":"ca-phe-den.jpg"},
{"id":2,"name":"Cà phê sữa","price":25000,"available":True,"image":"ca-phe-sua.jpg"},
{"id":3,"name":"Bạc xỉu","price":30000,"available":False,"image":"bac-xiu.jpg"},
{"id":4,"name":"Trà đào","price":35000,"available":True,"image":"tra-dao.jpg"},
{"id":5,"name":"Trà sữa","price":30000,"available":True,"image":"tra-sua.jpg"},
{"id":6,"name":"Nước cam","price":30000,"available":True,"image":"nuoc-cam.jpg"},
{"id":7,"name":"Sinh tố bơ","price":40000,"available":True,"image":"sinh-to-bo.jpg"}]
@app.context_processor
def shared_context(): return {"shop":SHOP}
@app.template_filter("vnd")
def vnd(value): return f"{value:,.0f}".replace(",",".")+" ₫"
@app.route("/")
def home():
    param=request.args.get("gio")
    if param is None: hour=datetime.now().hour
    else:
        try: hour=int(param)
        except ValueError: abort(400,description="Giờ phải là số nguyên từ 0 đến 23.")
        if not 0<=hour<=23: abort(400,description="Giờ phải là số nguyên từ 0 đến 23.")
    return render_template("index.html",promotions=PROMOTIONS,hour=hour)
@app.route("/menu")
def menu():
    per_page=3; pages=max(1,(len(MENU)+per_page-1)//per_page)
    page=request.args.get("page",default=1,type=int)
    if page<1 or page>pages: abort(404)
    start=(page-1)*per_page
    return render_template("menu.html",items=MENU[start:start+per_page],menu=MENU,page=page,pages=pages)
@app.route("/contact")
def contact(): return render_template("contact.html")
@app.errorhandler(404)
def page_not_found(error): return render_template("404.html"),404
if __name__=="__main__": app.run(debug=True)
