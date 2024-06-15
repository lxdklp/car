#include <iostream>
#include <fstream>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>
#include <cstring>
#include <cstdlib>
#include <string>
#include <sstream>

// 获取设备IP地址
std::string getIPAddress() {
    std::string ipAddress;
    FILE *fp = popen("hostname -I | awk '{print $1}'", "r");
    if (fp) {
        char buffer[128];
        while (fgets(buffer, sizeof(buffer), fp) != nullptr) {
            ipAddress += buffer;
        }
        pclose(fp);
    }
    // 移除结尾的换行符
    ipAddress.erase(ipAddress.find_last_not_of("\n") + 1);
    return ipAddress;
}

int main() {
    const char *inputFile = "/home/lckfb/car/send";
    const char *serialDevice = "/dev/ttyS3";
    const speed_t baudRate = B9600;

    // 打开串口设备文件
    int serialFd = open(serialDevice, O_RDWR | O_NOCTTY | O_NDELAY);
    if (serialFd == -1) {
        std::cerr << "无法打开串口设备文件: " << serialDevice << std::endl;
        return 1;
    }

    // 配置串口参数
    struct termios options;
    tcgetattr(serialFd, &options);
    cfsetispeed(&options, baudRate);
    cfsetospeed(&options, baudRate);
    options.c_cflag |= (CLOCAL | CREAD);
    options.c_cflag &= ~PARENB;
    options.c_cflag &= ~CSTOPB;
    options.c_cflag &= ~CSIZE;
    options.c_cflag |= CS8;
    tcsetattr(serialFd, TCSANOW, &options);

    while (true) {
        std::ifstream inFile(inputFile);
        if (!inFile) {
            std::cerr << "无法打开输入文件: " << inputFile << std::endl;
            close(serialFd);
            return 1;
        }

        std::string line;
        std::getline(inFile, line);
        inFile.close();

        if (line.empty()) {
            std::cerr << "读取到空行" << std::endl;
            usleep(100000); // 休眠以避免过快读取
            continue;
        }

        std::stringstream ss(line);
        int keyCode;
        ss >> keyCode;

        if (ss.fail() || !ss.eof()) {
            std::cerr << "读取键码失败或键码格式错误: " << line << std::endl;
            usleep(100000); // 休眠以避免过快读取
            continue;
        }

        std::string message;

        // 发送键码
        message = std::to_string(keyCode) + "\n";
        ssize_t bytesWritten = write(serialFd, message.c_str(), message.length());
        if (bytesWritten == -1) {
            std::cerr << "写入串口失败" << std::endl;
            close(serialFd);
            return 1;
        }

        // 当键码为15时，获取并发送IP地址
        if (keyCode == 15) {
            usleep(100000); // 0.1秒间隙

            std::string ipAddress = getIPAddress();
            if (ipAddress.empty()) {
                std::cerr << "获取IP地址失败" << std::endl;
                continue;
            }

            message = ipAddress + "\n";
            bytesWritten = write(serialFd, message.c_str(), message.length());
            if (bytesWritten == -1) {
                std::cerr << "写入串口失败" << std::endl;
                close(serialFd);
                return 1;
            }
        }

        // 休眠一段时间以避免文件读取过快
        usleep(100000); // 100毫秒
    }

    // 关闭串口文件描述符
    close(serialFd);

    return 0;
}