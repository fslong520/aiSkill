#include <bits/stdc++.h>
using namespace std;

struct Node {
    char val;
    Node *left, *right;
    Node(char v) : val(v), left(nullptr), right(nullptr) {}
};

// 根据前序和中序建树
Node* build(string preorder, string inorder) {
    if (preorder.empty()) return nullptr;
    
    char root = preorder[0];
    int pos = inorder.find(root);
    
    string inL = inorder.substr(0, pos);
    string inR = inorder.substr(pos + 1);
    string preL = preorder.substr(1, inL.size());
    string preR = preorder.substr(1 + inL.size());
    
    Node* node = new Node(root);
    node->left = build(preL, inL);
    node->right = build(preR, inR);
    return node;
}

// 判断两棵子树是否互为镜像
bool isMirror(Node* a, Node* b) {
    if (!a && !b) return true;
    if (!a || !b) return false;
    if (a->val != b->val) return false;
    return isMirror(a->left, b->right) && isMirror(a->right, b->left);
}

void freeTree(Node* root) {
    if (!root) return;
    freeTree(root->left);
    freeTree(root->right);
    delete root;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    string preorder, inorder;
    cin >> preorder >> inorder;
    
    Node* root = build(preorder, inorder);
    
    if (isMirror(root->left, root->right)) {
        cout << "Yes" << endl;
    } else {
        cout << "No" << endl;
    }
    
    freeTree(root);
    
    return 0;
}
