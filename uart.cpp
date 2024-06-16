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
    const char *inputFile = "/home/lckfb/car/send"; // 输入文件路径
    const char *serialDevice = "/dev/ttyS3"; // 串口设备路径
    const speed_t baudRate = B9600; // 波特率
    int lastKeyCode = -1; // 用于存储上次发送的键码

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
        // 打开输入文件
        std::ifstream inFile(inputFile);
        if (!inFile) {
            std::cerr << "无法打开输入文件: " << inputFile << std::endl;
            close(serialFd);
            return 1;
        }

        // 读取文件中的一行
        std::string line;
        std::getline(inFile, line);
        inFile.close();

        int keyCode;
        if (line.empty()) {
            // 如果文件为空且无上次发送数据，则继续读取
            if (lastKeyCode == -1) {
                std::cerr << "文件为空且无上次发送数据" << std::endl;
                usleep(10000); // 休眠10毫秒以避免过快读取
                continue;
            }
            keyCode = lastKeyCode; // 使用上次发送的数据
        } else {
            // 解析读取的键码
            std::stringstream ss(line);
            ss >> keyCode;

            if (ss.fail() || !ss.eof()) {
                std::cerr << "读取键码失败或键码格式错误: " << line << std::endl;
                usleep(10000); // 休眠10毫秒以避免过快读取
                continue;
            }

            lastKeyCode = keyCode; // 更新上次发送的数据
        }

        // 构建要发送的消息
        std::string message = std::to_string(keyCode) + "\n";
        ssize_t bytesWritten = write(serialFd, message.c_str(), message.length());
        if (bytesWritten == -1) {
            std::cerr << "写入串口失败" << std::endl;
            close(serialFd);
            return 1;
        }

        // 当键码为15时，获取并发送IP地址
        if (keyCode == 15) {
            usleep(10000); // 0.01秒间隙

            // 获取IP地址
            std::string ipAddress = getIPAddress();
            if (ipAddress.empty()) {
                std::cerr << "获取IP地址失败" << std::endl;
                continue;
            }

            // 延时0.01秒
            usleep(10000); // 0.01秒间隙

            // 发送IP地址
            message = ipAddress + "\n";
            bytesWritten = write(serialFd, message.c_str(), message.length());
            if (bytesWritten == -1) {
                std::cerr << "写入串口失败" << std::endl;
                close(serialFd);
                return 1;
            }
        }

        // 休眠10毫秒以避免文件读取过快
        usleep(10000); // 10毫秒
    }

    // 关闭串口文件描述符
    close(serialFd);

    return 0;
}