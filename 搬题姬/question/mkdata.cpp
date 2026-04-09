#include <bits/stdc++.h>
#include "mkin.h"

void mk_in() {
    // 创建testdata目录
    if (system("rm -rf testdata/*.in testdata/*.out testdata/*.zip") != 0) {
        cerr << "清理旧数据失败" << endl;
    }
    
    if (system("mkdir -p testdata") != 0) {
        cerr << "创建testdata目录失败" << endl;
        return;
    }

    cout << "开始生成输入数据..." << endl;
    for (int i = 1; i <= TEST_CASES; ++i) {
        string in_name = "testdata/" + to_string(i) + ".in";
        ofstream fout(in_name);
        if (!fout) {
            cerr << "无法打开文件 " + in_name << endl;
            continue;
        }
        
        test(i, fout);
        fout.close();
        cout << "生成【" << setw(2) << setfill('0') << i << ".in】数据成功" << endl;
    }
    cout << "输入数据生成完成" << endl << endl;
}

void mk_out() {
    cout << "开始生成输出数据..." << endl;
    for (int i = 1; i <= TEST_CASES; ++i) {
        string in_name = "testdata/" + to_string(i) + ".in";
        string out_name = "testdata/" + to_string(i) + ".out";
        string cmd = "./std < " + in_name + " > " + out_name;
        
        // 显示当前处理进度
        cout << "处理测试用例 【" << setw(2) << setfill('0') << i << "】...";
        cout.flush();
        
        int result = system(cmd.c_str());
        if (result != 0) {
            cerr << "\n生成【" << setw(2) << setfill('0') << i << ".out】数据失败" << endl;
        } else {
            cout << " 完成" << endl;
        }
    }
    cout << "输出数据生成完成" << endl;
}

int main() {
    // 编译标准程序
    cout << "编译标准程序..." << endl;
    if (system("g++ std.cpp -o std -std=c++17") != 0) {
        cerr << "编译标准程序失败" << endl;
        return 1;
    }
    cout << "编译标准程序成功" << endl << endl;

    mk_in();
    mk_out();
    
    // 清理可执行文件
    if (system("rm -f std") != 0) {
        // 非致命错误，不终止程序
        cout << "清理临时文件失败" << endl;
    }
    
    return 0;
}