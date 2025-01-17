import requests
import json
import time
import os
from lxml import etree
import re
import globalVar


def getHtml_DaQiaoRen(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Cookie': 'PHPSESSID=2v9vgarlcr4v548jutpm7hoo71; BdXlz_auth=72fcx39rm9PWLzHuPkmVGGXyyIFBIyPeFRNuC439s2vjPwYE8HQI2qtc-444iWXMCcv6KQhBNK2o57kR_I-0ESMIhJJ_c0u1dOHvdDBBEXgVdOXbb_aHX5CYrljFXMabClgulns1g1tFgL4D5wVRA6WgmHe-; BdXlz__userid=4120wofNOdiQra-Jsysz2lIo8NzxKQo2PqiMfkBf9tYU; BdXlz__username=3d778wTBLkaquEzT7ClQc1cxtyPdj3CF0rxz5b-Yw6SydA; BdXlz__groupid=73cbgKhSXlxR-NHYVIWzx3lI4KHNfw3CWP29B21K; BdXlz__nickname=74d6B6ViHuGpBIiAXHgiQ3VKowhgMZ-hWeni2lF3G10gTTDRKBMSfKpVgfvXXC4A',
        'Referer': 'http: // www.daqiaoren.com / index.php?m = content & c = index & a = lists & catid = 124'
    }

    # url = "http://www.daqiaoren.com/index.php?m=member&c=index&a=login"
    # url = "http://www.daqiaoren.com//index.php?m=content&c=index&a=lists&catid=15"
    # exam_url_1st = "http://www.daqiaoren.com//index.php?m=content&c=index&a=lists&catid=9"

    # exam_url_A = 'http://www.daqiaoren.com/index.php?m=content&c=index&a=show&catid=125&id=3409'
    exam_url_A = url
    html_exam_url_A = requests.get(exam_url_A, headers=headers)
    # print(html_exam_url_A.text)
    return html_exam_url_A.text


def htmlAnalysis_DaQiaoRenQusetionBank(htmlText):
    resDic = {}
    # parser = etree.HTMLParser(encoding='utf-8')
    # tree = etree.parse(htmlPath, parser=parser)
    numberRegx = r'\d*'
    tree = etree.HTML(htmlText)
    htmlAnalysis_question = tree.xpath("/html/body/div//h1/span//text()")
    index = 0
    try:
        index = re.findall(numberRegx, htmlAnalysis_question[0])[0]
    except IndexError:
        pass
    index = int(index)
    htmlAnalysis_question_new = [index, ''.join(htmlAnalysis_question[1:])]
    # print('htmlAnalysis_question:', htmlAnalysis_question_new)

    htmlAnalysis_questionImg = tree.xpath("/html/body/div//div[@class='tiimg']/img/@src")
    try:
        htmlAnalysis_questionImg_new = htmlAnalysis_questionImg[0]
    except IndexError:
        htmlAnalysis_questionImg = tree.xpath("/html/body/div//h1/span//@src")
        try:
            htmlAnalysis_questionImg_new = htmlAnalysis_questionImg[0]
        except IndexError:
            htmlAnalysis_questionImg_new = ''
    # print('htmlAnalysis_questionImg:', htmlAnalysis_questionImg_new)

    htmlAnalysis_options = tree.xpath("/html/body/div//ul[@id='ul_answers']/label//text()")
    htmlAnalysis_options_new = []
    opStr = ''.join(htmlAnalysis_options)
    htmlAnalysis_options_new = re.sub(globalVar.regxOptions_group, '\\n', opStr, 0, re.MULTILINE)
    htmlAnalysis_options_new = re.findall(r'.+', htmlAnalysis_options_new)
    # for op in htmlAnalysis_options:
    #     if len(op.strip().replace(r'\r\n', '')) > 0:
    #         htmlAnalysis_options_new.append(op)
    # print('htmlAnalysis_options_new:', htmlAnalysis_options_new)
    # print('type:', type(htmlAnalysis_options_new))
    # for index, tem in htmlAnalysis_options_new:
    #     print('index:', index, '。tem:', tem)

    htmlAnalysis_answer = tree.xpath("/html/body/div//div[@class='daanjiexi']/p//text()")
    htmlAnalysis_answer_new = []
    try:
        htmlAnalysis_answer_new.append(htmlAnalysis_answer[0])
    except IndexError:
        # 答案解析中只有图片时，无法识别答案
        # print('需要手动在answer中标注答案')
        htmlAnalysis_answer_new = ['', '']
    else:
        try:
            htmlAnalysis_answer_new.append(''.join(htmlAnalysis_answer[1:]))
        except IndexError:
            pass
    # print('htmlAnalysis_answer:', htmlAnalysis_answer_new)
    htmlAnalysis_answerImg = tree.xpath("/html/body/div//div[@class='daanjiexi']/p/img/@src")
    try:
        htmlAnalysis_answerImg_new = htmlAnalysis_answerImg[0]
    except IndexError:
        htmlAnalysis_answerImg_new = ''


    # htmlAnalysis_questionUrl = tree.xpath("/html/body/header//div[@class='div3']//a/@href")
    # print('htmlAnalysis_questionUrl:', htmlAnalysis_questionUrl)

    resDic['htmlAnalysis_question'] = htmlAnalysis_question_new
    resDic['htmlAnalysis_questionImg'] = htmlAnalysis_questionImg_new
    resDic['htmlAnalysis_options'] = htmlAnalysis_options_new
    resDic['htmlAnalysis_answer'] = htmlAnalysis_answer_new
    resDic['htmlAnalysis_answerImg'] = htmlAnalysis_answerImg_new
    print(resDic)
    return resDic


def saveAsJson(path, name, index: int, question, questionImgUrl, options: list, answer: str, detail):
    pass


def getOptionsDic(questionType, name, index: int, question, questionImgUrl, options: list, answer: str, detail, detaiImglUrl):
    # answer=['contentA', 'contentB', 'contentC']
    errorList = []
    dic = {}
    res = {'optionsDic': dic, 'error': errorList}

    answer = answer.upper()
    answerList = []
    optionsDic = {}
    regxName = globalVar.regxOptionsABCDE
    regxContent = globalVar.regxOptionsABCDE_except
    # 以下组装answerList
    for option in options:
        try:
            answerName = re.findall(regxName, option)[0].upper()
        except IndexError:
            print('选项错误')
            error = f'option:{option}选项错误'
            errorList.append(error)
        else:
            optionsDic['name'] = answerName
            try:
                answerContent = re.findall(regxContent, option)[0]
            except IndexError:
                pass
            else:
                optionsDic['content'] = answerContent
            # print('answer:', answer)
            # print('answerName:', answerName)
            if answer.find(answerName) >= 0:
                optionsDic['isanswer'] = True
            else:
                optionsDic['isanswer'] = False
            answerList.append(optionsDic)
            optionsDic = {}
    if re.match(globalVar.regexIsUrl, questionImgUrl) is not None:
        status = download_img(questionImgUrl)
    # if status:
        question = question + f'<img src="https://gitee.com/yuebulv/picture/raw/master/yantu/{os.path.basename(questionImgUrl)}">'

    if re.match(globalVar.regexIsUrl, detaiImglUrl) is not None:
        status = download_img(detaiImglUrl)
    # if status:
        detail = detail + f'<img src="https://gitee.com/yuebulv/picture/raw/master/yantu/{os.path.basename(detaiImglUrl)}">'
    dic = {
        "type": questionType,
        "id": 0,
        "name": name,
        "content": question,
        "answer": answerList,
        'detail': detail,
        'index': index
    }
    # print(dic)
    # json.dump(dic, open(path, 'a', encoding='utf-8', newline='\n'), indent=4, ensure_ascii=False)
    res = {'optionsDic': dic, 'error': errorList}
    return res


def download_img(img_url):
    status = False
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Cookie': 'PHPSESSID=2v9vgarlcr4v548jutpm7hoo71; BdXlz_auth=72fcx39rm9PWLzHuPkmVGGXyyIFBIyPeFRNuC439s2vjPwYE8HQI2qtc-444iWXMCcv6KQhBNK2o57kR_I-0ESMIhJJ_c0u1dOHvdDBBEXgVdOXbb_aHX5CYrljFXMabClgulns1g1tFgL4D5wVRA6WgmHe-; BdXlz__userid=4120wofNOdiQra-Jsysz2lIo8NzxKQo2PqiMfkBf9tYU; BdXlz__username=3d778wTBLkaquEzT7ClQc1cxtyPdj3CF0rxz5b-Yw6SydA; BdXlz__groupid=73cbgKhSXlxR-NHYVIWzx3lI4KHNfw3CWP29B21K; BdXlz__nickname=74d6B6ViHuGpBIiAXHgiQ3VKowhgMZ-hWeni2lF3G10gTTDRKBMSfKpVgfvXXC4A',
        'Referer': 'http: // www.daqiaoren.com / index.php?m = content & c = index & a = lists & catid = 124'
    }
    r = requests.get(img_url, headers=headers, stream=True)
    # print(r.status_code) # 返回状态码
    if r.status_code == 200:
        open(f'.\data\picture\{os.path.basename(img_url)}', 'wb').write(r.content)  # 将内容写入图片
        print("done")
        status = True
    del r
    return status


def geturl_DaQiaoRen(url, headers, xpathStr):
    pass
    '''
    http://www.daqiaoren.com/index.php?m=content&c=index&a=lists&catid=9
    # 2020 http://www.daqiaoren.com/index.php?m=content&c=index&a=lists&catid=124
        http://www.daqiaoren.com/index.php?m=content&c=index&a=show&catid=125&id=3409
        http://www.daqiaoren.com/index.php?m=content&c=index&a=show&catid=126&id=3479
    # 2019 http://www.daqiaoren.com/index.php?m=content&c=index&a=lists&catid=44
        http://www.daqiaoren.com/index.php?m=content&c=index&a=show&catid=45&id=1312
        http://www.daqiaoren.com/index.php?m=content&c=index&a=show&catid=46&id=1382
    # 2018 http://www.daqiaoren.com/index.php?m=content&c=index&a=lists&catid=19
        # http://www.daqiaoren.com/index.php?m=content&c=index&a=show&catid=20&id=205
        # http://www.daqiaoren.com/index.php?m=content&c=index&a=show&catid=21&id=275
    # 2017 http://www.daqiaoren.com/index.php?m=content&c=index&a=lists&catid=26
        # http://www.daqiaoren.com/index.php?m=content&c=index&a=show&catid=27&id=405
        # http://www.daqiaoren.com/index.php?m=content&c=index&a=show&catid=28&id=543
    '''
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    #     'Cookie': 'PHPSESSID=2v9vgarlcr4v548jutpm7hoo71; BdXlz_auth=72fcx39rm9PWLzHuPkmVGGXyyIFBIyPeFRNuC439s2vjPwYE8HQI2qtc-444iWXMCcv6KQhBNK2o57kR_I-0ESMIhJJ_c0u1dOHvdDBBEXgVdOXbb_aHX5CYrljFXMabClgulns1g1tFgL4D5wVRA6WgmHe-; BdXlz__userid=4120wofNOdiQra-Jsysz2lIo8NzxKQo2PqiMfkBf9tYU; BdXlz__username=3d778wTBLkaquEzT7ClQc1cxtyPdj3CF0rxz5b-Yw6SydA; BdXlz__groupid=73cbgKhSXlxR-NHYVIWzx3lI4KHNfw3CWP29B21K; BdXlz__nickname=74d6B6ViHuGpBIiAXHgiQ3VKowhgMZ-hWeni2lF3G10gTTDRKBMSfKpVgfvXXC4A',
    #     'Referer': 'http: // www.daqiaoren.com / index.php?m = content & c = index & a = lists & catid = 124'
    # }
    # url = 'http://www.daqiaoren.com/index.php?m=content&c=index&a=lists&catid=9'
    # xpathStr = "/html/body/a/@href"
    html = requests.get(url, headers=headers)
    tree = etree.HTML(html.text)
    htmlAnalysis = tree.xpath(xpathStr)
    return htmlAnalysis


def url_zhishiPaper(headers, htmlAnalysis):
    # 根据urllist拼接得到知识真题url
    list_zhishiPaper = []
    dic_zhishiPaper = {}
    for url_temp in htmlAnalysis:
        name_A = geturl_DaQiaoRen(url_temp, headers, "/html/body/h3[1]/text()")[0]
        url_A = geturl_DaQiaoRen(url_temp, headers, "/html/body/ul[1]/li[1]/a[1]/@href")[0]
        name_B = geturl_DaQiaoRen(url_temp, headers, "/html/body/h3[2]/text()")[0]
        url_B = geturl_DaQiaoRen(url_temp, headers, "/html/body/ul[2]/li[1]/a[1]/@href")[0]
        dic_zhishiPaper['name_A'] = name_A
        dic_zhishiPaper['url_A'] = url_A
        list_zhishiPaper.append(dic_zhishiPaper)
        dic_zhishiPaper = {}
        dic_zhishiPaper['name_A'] = name_B
        dic_zhishiPaper['url_A'] = url_B
        # print(dic_zhishiPaper)
        list_zhishiPaper.append(dic_zhishiPaper)
        dic_zhishiPaper = {}
    return list_zhishiPaper


def spider_DqQiaoRen(saveName, url):
    pass


def getQuestionDic(url):
    # with open('test.html', 'r', encoding='utf-8') as htmlFile:
    #     htmlText = htmlFile.read()
    # htmlPath = 'test.html'
    # htmlAnalysis_DaQiaoRenQusetionBank(htmlPath)
    errorList = []
    questionDic = {}
    res = {'questionDic': questionDic, 'error': errorList}
    exam_url_A = url  # 'http://www.daqiaoren.com/index.php?m=content&c=index&a=show&catid=125&id=3409'
    temp1 = getHtml_DaQiaoRen(exam_url_A)
    questionDic = htmlAnalysis_DaQiaoRenQusetionBank(temp1)

    # questionType = ['单选题', '多选题']
    questionTypeSet = {'单选题': 0, '多选题': 1}
    name = ''
    index = questionDic['htmlAnalysis_question'][0]
    # img
    question = questionDic['htmlAnalysis_question'][1]
    questionImgUrl = questionDic['htmlAnalysis_questionImg']
    for typeEl in questionTypeSet:
        if question.find(typeEl) >= 0:
            name = typeEl
            questionType = questionTypeSet[typeEl]
            break
    options = questionDic['htmlAnalysis_options']
    try:
        answer = re.findall(globalVar.regxAnswer, questionDic['htmlAnalysis_answer'][0])[0]
    except IndexError:
        answer = ''
        errorList.append('答案解析中有可能是图片,需要手动在answer中标注答案')
        print('答案解析中有可能是图片,需要手动在answer中标注答案')
        print('imgurl:',questionDic['htmlAnalysis_answerImg'])
        # return '错误'
    detail = ''
    try:
        detail = questionDic['htmlAnalysis_answer'][1]
    except IndexError:
        pass
    questionDic_dic = getOptionsDic(questionType=questionType, name=name, index=index, question=question,
                                questionImgUrl=questionImgUrl, options=options, answer=answer, detail=detail,
                                detaiImglUrl=questionDic['htmlAnalysis_answerImg'])
    questionDic = questionDic_dic['optionsDic']
    # print(questionDic_dic)
    if questionDic_dic['error']:
        errorList.append('\\t'.join(questionDic_dic['error']))
    # dic['content'] = 'temp'
    # print(dic)
    res = {'questionDic': questionDic, 'error': errorList}
    return res


if __name__ == '__main__':
    errorList = []
    res = {'error': errorList}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Cookie': 'PHPSESSID=2v9vgarlcr4v548jutpm7hoo71; BdXlz_auth=72fcx39rm9PWLzHuPkmVGGXyyIFBIyPeFRNuC439s2vjPwYE8HQI2qtc-444iWXMCcv6KQhBNK2o57kR_I-0ESMIhJJ_c0u1dOHvdDBBEXgVdOXbb_aHX5CYrljFXMabClgulns1g1tFgL4D5wVRA6WgmHe-; BdXlz__userid=4120wofNOdiQra-Jsysz2lIo8NzxKQo2PqiMfkBf9tYU; BdXlz__username=3d778wTBLkaquEzT7ClQc1cxtyPdj3CF0rxz5b-Yw6SydA; BdXlz__groupid=73cbgKhSXlxR-NHYVIWzx3lI4KHNfw3CWP29B21K; BdXlz__nickname=74d6B6ViHuGpBIiAXHgiQ3VKowhgMZ-hWeni2lF3G10gTTDRKBMSfKpVgfvXXC4A',
        'Referer': 'http: // www.daqiaoren.com / index.php?m = content & c = index & a = lists & catid = 124'
    }
    url = 'http://www.daqiaoren.com/index.php?m=content&c=index&a=lists&catid=9'
    xpathStr = "/html/body/a/@href"
    url_list = geturl_DaQiaoRen(url, headers, xpathStr)

    url_dic_list = url_zhishiPaper(headers, url_list[1:2])

    regxPage = r'=(\d*)$'
    regxUrl = r'(.+=)\d*$'
    for url_dic in url_dic_list:
        saveName_A = url_dic['name_A']
        # saveName_B = url_dic['name_B']
        url_A0 = url_dic['url_A']
        # url_B0 = url_dic['url_B']
        url_noPage = re.findall(regxUrl, url_A0)[0]
        page_A0 = int(re.findall(regxPage, url_A0)[0])
        path = f'./data/{saveName_A}.json'
        res_question_dic_list = []
        for i in range(70):
            url_A_new = url_noPage + str(page_A0+i)

            questionDic_dic_includeError = getQuestionDic(url_A_new)
            questionDic = questionDic_dic_includeError['questionDic']

            if questionDic_dic_includeError['error']:
                print(questionDic_dic_includeError)
                error = saveName_A + f'第{i+1}题' + '\\t'.join(questionDic_dic_includeError['error'])
                errorList.append(error)
            # print(questionDic_dic)
            # questionDic = questionDic_dic['questionDic']

            # if questionDic_dic['error']:
            #     error = saveName_A + f'第{i}题' + '\\t'.join(questionDic_dic['error'])
            #     errorList.append(error)
            res_question_dic_list.append(questionDic)
        # 保存
        json.dump(res_question_dic_list, open(path, 'a', encoding='utf-8', newline='\n'), indent=4, ensure_ascii=False)
    with open('./log/log.txt', 'a') as fp:
        # fp.writelines(errorList)
        for temp in errorList:
            fp.write(temp)
            fp.write('\r')