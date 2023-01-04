## How to install Nginx in Linux
### 1.Download Nginx and its dependencies
下载到当前用户目录
#### 1.1.pcre2
```
wget github.com/PCRE2Project/pcre2/releases/download/pcre2-10.42/pcre2-10.42.tar.gz
```
#### 1.2.zlib
```
wget http://zlib.net/zlib-1.2.13.tar.gz
```
#### 1.3.openssl
```
wget https://github.com/openssl/openssl/archive/refs/tags/openssl-3.1.0-beta1.zip
```
#### 1.4.nginx
```
wget https://nginx.org/download/nginx-1.23.3.tar.gz
```

### 2.解压缩
```
tar -zxf pcre2-10.42.tar.gz  
tar -zxf zlib-1.2.13.tar.gz  
unzip openssl-3.1.0-beta1.zip  
tar -zvf nginx-1.23.3.tar.gz  
```

### 3.新增用户和组
Nginx 启动后会出现两种进程，分别是主进程（master process）和工作进程（worker process）。前者只有一个，作用是读取、估算配置，以及管理工作进程。后者可以有多个（个数可通过配置文件中的指令 worker_processes 进行设置），作用是处理请求。

主进程要以管理员账户（root）的身份运行。这是因为在 Linux 系统中，绑定低于 1024 的本地 TCP 端口号必须使用管理员账户（root）权限，而 Web 服务器所使用的 HTTP 协议和 HTTPS 协议的默认端口分别是 80 和 443，Nginx 要绑定这两个端口号，就必须有管理员账户权限。另外，还需要 root 权限读取配置文件。

而工作进程则需要以普通用户身份运行。这是因为实际处理请求的是工作进程，限制其权限可以避免出现危及操作系统安全的潜在隐患。该账户通常是 Web 服务器专用账户，如 www-data（接下来会在 Nginx 的配置文件中设定），一般与 FastCGI 程序（如 PHP-FPM）所使用的账户相同。
```
sudo groupadd nginx  
sudo useradd -M -s /sbin/nologin -g nginx nginx
```

### 4.执行./configure
```
cd nginx-1.23.3

./configure --user=nginx \
--with-pcre=../pcre2-10.42 \
--with-openssl=../openssl-openssl-3.1.0-beta1 \
--with-zlib=../zlib-1.2.13 \
--with-http_ssl_module \
--with-http_realip_module \
--with-http_addition_module \
--with-http_sub_module \
--with-http_dav_module \
--with-http_mp4_module \
--with-http_flv_module \
--with-http_gzip_static_module \
--with-http_random_index_module \
--with-http_secure_link_module \
--with-http_stub_status_module \
--with-mail --with-mail_ssl_module \
--with-file-aio \
--with-http_v2_module \
--with-http_auth_request_module \
--with-http_gunzip_module \
--with-http_degradation_module \
--with-http_slice_module \
--with-stream=dynamic \
--with-stream_ssl_module \
--with-debug
```

### 5.执行make
```
make
```

### 6.执行make install
```
sudo make install
```

### 7.建立nginx软链接
```
sudo ln -s /usr/local/nginx/sbin/nginx /usr/bin
```

### 8.系统自启动
```
sudo vim /etc/systemd/system/nginx.service  
```
拷贝以下内容到上述新建文件，  
```
[Unit]  
Description=The NGINX HTTP and reverse proxy server  
After=syslog.target network.target remote-fs.target nss-lookup.target  

[Service]  
Type=forking  
ExecStartPre=/usr/local/nginx/sbin/nginx -t  
ExecStart=/usr/local/nginx/sbin/nginx  
ExecReload=/bin/kill -s HUP $MAINPID  
ExecStop=/bin/kill -s QUIT $MAINPID  

[Install]  
WantedBy=multi-user.target  
```

运行以下命令，让 systemd 读取新创建的配置文件， 

```
systemctl daemon-reload  
systemctl enable nginx  
```

### 9.Nginx启停
```
systemctl start nginx  
systemctl restart nginx  
systemctl reload nginx | nginx -s reload  
systemctl status nginx
```