import os
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files import File
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from moviepy.editor import VideoFileClip, concatenate_videoclips

from .models import Message
from .forms import PostForm
import datetime
import subprocess
import openai
# from langchain_openai import ChatOpenAI



# ユーザー認証関数
def top(request):
    a =  1
    return render(request, 'sns/top.html')


# indexのビュー関数
#@login_required(login_url='/accounts/login/')
def index(request):
    # POST送信時の処理
    print('index❶')
    messages = Message.objects.all
    print('messages:',messages)
    #  共通処理
    params = {
       'contents': messages,
    }
    return render(request, 'sns/index.html', params)


# メッセージのポスト処理
#@login_required(login_url='/accounts/login/')
def post(request):
    # POST送信の処理
    if request.method == 'POST':
        # 送信内容の取得
        # gr_name = request.POST['groups']
        content = request.POST['content']
        photo1 = request.FILES.get('photo1')

        # OpenAI APIを使って質問に対する回答を取得
        if str(request.user) != 'ZZZ':
            response = openai.ChatCompletion.create(
                model="gpt-4",  # 使用するモデル (例えば、gpt-4)
                messages=[
                    {"role": "system", "content": " helpful assistant."},
                    {"role": "user", "content": content}
                ]
            )
            # 回答を取得し、answerに格納
            aianswer = response['choices'][0]['message']['content']
            print(aianswer)


# Groupの取得
       # Messageを作成し設定して保存
        msg = Message()
        msg.author = request.user
        msg.content = content
        msg.aianswer = aianswer
        msg.photo1 = photo1
        msg.save()

        # メッセージを設定
        messages.success(request, '新しいメッセージを投稿しました！')
        # メール送付
        subject = "Private-SNS"
        honbun =  str(request.user) + 'さんから新しいメッセージが投稿されました'
        from_mail = "sh-ninomiya@c02.itscom.net"
        to_mail_list = [
               'sh-ninomiya@c02.itscom.net'
        ]
        email = EmailMessage(subject, honbun, from_mail, to_mail_list)
     #   email.send()

        # *************************** これからAIchat *******************************
        return redirect(to='index')

    # GETアクセス時の処理
    else:
        form = PostForm()
        # print('Post7')
    # 共通処理
    params = {
        'login_user': request.user,
        'form': form,
    }
    return render(request, 'sns/post.html', params)

def delete(request, num):
    print('delete❶ num=', num)
    if (request.method == 'POST'):
        # msgid = request.GET['msg_id']
        obj = Message.objects.get(id=num)
        obj.delete()
        print('delete❸ num=',num)
        messages.success(request, 'メッセージを削除しました！')
        return redirect(to='index')
    else:
        obj = Message.objects.get(id=num)
        print('delete❷ num=', num)
        # フォームの各フィールドに値を手動でセット
        form = PostForm()
        form.fields['content'].initial = obj.content
        params = {
            # 'msgid': msgid,
            'message': obj,
            'form': form
            }
        return render(request, 'sns/delete.html', params)

def edit(request, num):
    obj = Message.objects.get(id=num)
    if request.method == 'POST':
        # 送信内容の取得
        content = request.POST['content']
        photo1 = request.FILES.get('photo1')
        # Groupの取得
        # print('edit❶ _gr_name;',gr_name,'group;',group,content)
        # Messageを作成し設定して保存
        obj.content = content
        if photo1 != None:
            obj.photo1 = photo1
        obj.save()
        # メッセージを設定
        messages.success(request, 'メッセージを編集しました！')
        return redirect(to='index')
    # GETリクエスト
    else:

            # フォームの各フィールドに値を手動でセット
            form = PostForm()
            form.fields['content'].initial = obj.content
            # form.fields['groups'].initial = obj.group
            form.fields['photo1'].initial = obj.photo1
            # form.fields['photo2'].initial = obj.photo2
            params = {
                'message': obj,
                'form': form
            }
            return render(request, 'sns/edit.html', params)


def comment(request):
    if request.method == 'POST':
        content = request.POST['cmt']
        print("comment❶")
        cmnt = Comment()
        cmnt.text = content
        cmnt.commented_to = Message.objects.get(id=request.GET['msg_id'])
        cmnt.commented_by = request.user
        cmnt.save()
        # コメントを投稿しました
        # messages.success(request,'新しいコメントを投稿しました！')
        return redirect(to='index')
    # GETリクエスト
    else:
        print('cmment❷')
        msgid = request.GET['msg_id']
        # owner = request.GET['owner']
        the_message = Message.objects.get(id=msgid)
        comments = Comment.objects.filter(commented_to=the_message)
        comments = Comment.objects.filter(commented_to=msgid)

        # form = CommentForm(request)

    params = {
        'msgid': msgid,
        'message': the_message,
        'comments': comments,
    }
    return render(request, 'sns/comment.html', params)

