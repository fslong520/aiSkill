#pragma once

#ifndef MKIN_H
#define MKIN_H

#include <bits/stdc++.h>
using namespace std;

const int TEST_CASES = 25;

struct Node {
    char val;
    Node *left, *right;
    Node(char v) : val(v), left(nullptr), right(nullptr) {}
};

// 递归建树（用于遍历输出）
void inorder(Node* root, string& s) {
    if (!root) return;
    inorder(root->left, s);
    s += root->val;
    inorder(root->right, s);
}

void preorder(Node* root, string& s) {
    if (!root) return;
    s += root->val;
    preorder(root->left, s);
    preorder(root->right, s);
}

void freeTree(Node* root) {
    if (!root) return;
    freeTree(root->left);
    freeTree(root->right);
    delete root;
}

// 构建对称树
Node* buildSymmetric(int depth, char& ch) {
    if (depth == 0) return nullptr;
    Node* root = new Node(ch++);
    root->left = buildSymmetric(depth - 1, ch);
    root->right = buildSymmetric(depth - 1, ch); // 简化：左右子树相同结构
    return root;
}

// 手动构造对称树样例
Node* buildSymmetricSample() {
    Node* root = new Node('A');
    root->left = new Node('B');
    root->right = new Node('B');
    root->left->left = new Node('D');
    root->left->right = new Node('E');
    root->right->left = new Node('E');
    root->right->right = new Node('D');
    return root;
}

void test(int case_num, ofstream& fout)
{
    if (case_num == 1)
    {
        // 样例：对称树
        fout << "ABDEBED" << endl;
        fout << "DBEAEBD" << endl;
    }
    else if (case_num == 2)
    {
        // 单节点：对称
        fout << "A" << endl;
        fout << "A" << endl;
    }
    else if (case_num == 3)
    {
        // 只有左子树：不对称
        fout << "AB" << endl;
        fout << "BA" << endl;
    }
    else if (case_num == 4)
    {
        // 满二叉树且对称
        fout << "ABB" << endl;
        fout << "BAB" << endl;
    }
    else if (case_num == 5)
    {
        // 满二叉树但不对称
        fout << "ABC" << endl;
        fout << "BAC" << endl;
    }
    else if (case_num % 2 == 0)
    {
        // 偶数用例：对称树
        fout << "ABB" << endl;
        fout << "BAB" << endl;
    }
    else
    {
        // 奇数用例：非对称树
        fout << "ABC" << endl;
        fout << "BAC" << endl;
    }
}

#endif
