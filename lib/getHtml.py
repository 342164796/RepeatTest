# -*- coding:utf-8 -*-
import time
def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
def get_tr(case_name,status,img,log):
    tr = '''
    <tr bgcolor="MintCream">
        %(case_name)s
        %(status)s
        %(img)s
        %(log)s
    </tr>
    '''
    case_name = '<td>{}</td>'.format(case_name)
    status = '<td>{}</td>'.format(status)
    img = '<td><img src="{}" align="absmiddle" width="480" height="270"/></td>'.format(img)
    log = '<td><a href="{}">device_log</a></td>'.format(log)
    result = {'case_name': case_name,'status':status, 'img': img,'log':log}
    return tr % result
def getHtml(tr,test_status,result_path):
    all_case, passed, failed = test_status
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="Content-type" content="text/html"; charset=utf-8"/>
        <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
        <title>Test Report</title>
    </head>
    <body>
    <span style="color:green;"><h1>Test Report</h1></span>
    <p>End Time:{Time}</p>
    <p><span style="color:blue;">All_Case:{All_Case},<span style="color:green;">passed:{passed},<span style="color:red;">failed:{failed}</p>
    <table>
    </table>
    <table border="1"
cellpadding="10">
        <tbody>
        <tr bgcolor="MintCream">
            <th>case_name</th>
            <th>result</th>
            <th>screenshot</th>
            <th>Log</th>
        </tr>
            %(tr)s
        </tbody>
    </table>
    </body>
    </html>
    '''.format(Time=get_time(),All_Case=all_case,passed=passed,failed=failed)
    data={'tr': tr}
    test_report = '%s/testReport.html' % result_path
    with open(test_report,'w') as f:
        f.write(template % data)
        f.close()
    return test_report
