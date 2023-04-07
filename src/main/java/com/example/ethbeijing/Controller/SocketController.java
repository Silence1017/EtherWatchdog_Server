package com.example.ethbeijing.Controller;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.example.ethbeijing.common.R;
import org.springframework.web.bind.annotation.*;

import java.io.*;
import java.net.InetAddress;
import java.net.Socket;

@RestController
@RequestMapping("/socket")
@CrossOrigin(origins = "*")
public class SocketController {
@GetMapping("/{hash}")
    public R<Object> get(@PathVariable String hash) throws IOException {
    JSONObject jsonObject = new JSONObject();
    jsonObject.put("hash", hash);
    String str = jsonObject.toJSONString();
    InetAddress addr = InetAddress.getLocalHost();
    String host= addr.getHostAddress();
    //String host="192.168.73.1";
    String res;
    //String ip=addr.getHostAddress().toString(); //获取本机ip
    //log.info("调用远程接口:host=>"+ip+",port=>"+12345);

    // 初始化套接字，设置访问服务的主机和进程端口号，HOST是访问python进程的主机名称，可以是IP地址或者域名，PORT是python进程绑定的端口号
    Socket socket = new Socket(host,12345);
    try {

        // 获取输出流对象
        OutputStream os = socket.getOutputStream();
        PrintStream out = new PrintStream(os);
        // 发送内容
        out.print(str);
        // 告诉服务进程，内容发送完毕，可以开始处理
        out.print("over");

        // 获取服务进程的输入流
        InputStream is = socket.getInputStream();
        BufferedReader br = new BufferedReader(new InputStreamReader(is,"utf-8"));
        String tmp = null;
        StringBuilder sb = new StringBuilder();
        // 读取内容
        while((tmp=br.readLine())!=null)
            sb.append(tmp).append('\n');
        System.out.print(sb);
        // 解析结果
        //res = JSON.toJSONString(sb.toString());
        String strr=sb.toString().replace("\n", "");
        System.out.println(strr);
        JSONObject object= JSONObject.parseObject(strr);

        return R.success(object);
    } catch (IOException  e) {
        e.printStackTrace();

    } finally {
        try {if(socket!=null) socket.close();} catch (IOException e) {}
        System.out.print("远程接口调用结束.");

    }
    return R.error("未知错误");

}
}
