import poplib
import email


"""
    需求：消息标题、附件名称（存在header中）都是以字节为单位进行传输的，中文内容需要解码
    功能：对header进行解码
"""
def decode(header: str):
    value, charset = email.header.decode_header(header)[0]
    if charset:
        return str(value, encoding=charset)
    else:
        return value


"""
    功能：下载某一个消息的所有附件
"""
def download_attachment(msg):
    subject = decode(msg.get('Subject'))  # 获取消息标题
    for part in msg.walk():  # 遍历整个msg的内容
        if part.get_content_disposition() == 'attachment':
            attachment_name = decode(part.get_filename())  # 获取附件名称
            attachment_content = part.get_payload(decode=True)  # 下载附件
            attachment_file = open('' + attachment_name, 'wb') # 在指定目录下创建文件，注意二进制文件需要用wb模式打开
            attachment_file.write(attachment_content)  # 将附件保存到本地
            attachment_file.close()
    print('Done………………', subject)


def main():

    """连接到POP3服务器"""
    with open('', 'r') as f1:
        config = f1.readlines()
    for i in range(0, len(config)):
        config[i] = config[i].rstrip('\n')

    # print(config)

    # POP3服务器、用户名、密码
    host = config[0]  # pop.163.com
    username = config[1]  # 用户名
    password = config[2]  # 密码

    # 连接到POP3服务器
    server = poplib.POP3(host)

    # 身份验证
    server.user(username)
    server.pass_(password)  # 参数是你的邮箱密码，如果出现poplib.error_proto: b'-ERR login fail'，就用开启POP3服务时拿到的授权码

    """获取邮箱中消息（邮件）数量"""
    msg_count, _ = server.stat()

    """遍历消息并保存附件"""
    for i in range(msg_count):
        """获取消息内容：POP3.retr(which)检索index为which的整个消息，并将其设为已读"""
        _, lines, _ = server.retr(
            i+1)  # 3个结果分别是响应结果（1个包含是否请求成功和该消息大小的字符串），消息内容（一个字符串列表，每个元素是消息内容的一行），消息大小（即有多少个octets，octet特指8bit的字节）

        """将bytes格式的消息内容拼接"""
        msg_bytes_content = b'\r\n'.join(lines)

        """将字符串格式的消息内容转换为email模块支持的格式（<class 'email.message.Message'>）"""
        msg = email.message_from_bytes(msg_bytes_content)

        """下载消息中的附件"""
        download_attachment(msg)


if __name__ == "__main__":
    main()
