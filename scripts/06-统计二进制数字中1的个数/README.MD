```c++
int get_bin_count(int s){
    int res = 0;
    while(s != 0){
        res += s & 1;// 如果s最后一位是1, 则和1做与操作也是1; 反之为0
        s = s >> 1;// 向右移动一位
    }
    return res;
}
```