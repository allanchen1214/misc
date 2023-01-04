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