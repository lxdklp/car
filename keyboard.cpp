#include <iostream>
#include <fstream>
#include <fcntl.h>
#include <unistd.h>
#include <linux/input.h>

int main() {
    const char *keyboardDevice = "/dev/input/event4"; // 使用具体的键盘设备文件
    const char *outputFile = "/home/lckfb/car/send";

    int fd = -1;
    struct input_event ie;

    while (true) {
        // 尝试打开键盘设备文件
        if (fd == -1) {
            fd = open(keyboardDevice, O_RDONLY);
            if (fd == -1) {
                // 如果无法打开键盘设备文件，向输出文件写入10
                std::ofstream outFile(outputFile);
                if (!outFile) {
                    std::cerr << "无法打开输出文件: " << outputFile << std::endl;
                    return 1;
                }
                outFile << 10 << std::endl;
                outFile.close();

                // 等待一段时间后再尝试重新打开键盘设备文件
                sleep(1);
                continue;
            }
        }

        // 读取输入事件
        ssize_t bytesRead = read(fd, &ie, sizeof(struct input_event));
        if (bytesRead == sizeof(struct input_event)) {
            // 只处理按键事件
            if (ie.type == EV_KEY && ie.value >= 0 && ie.value <= 2) {
                // 检查键码和状态的有效性，防止写入空行
                if (ie.code != 0 || ie.value != 0) {
                    // 打开输出文件（每次写入时覆盖）
                    std::ofstream outFile(outputFile);
                    if (!outFile) {
                        std::cerr << "无法打开输出文件: " << outputFile << std::endl;
                        close(fd);
                        fd = -1;
                        continue;
                    }

                    if (ie.value == 0) {
                        outFile << 41 << std::endl;
                    } else {
                        outFile << ie.code << std::endl;
                    }
                    outFile.close(); // 立即关闭文件
                }
            }
        } else {
            std::cerr << "读取输入事件失败" << std::endl;
            close(fd);
            fd = -1;
        }
    }

    return 0;
}