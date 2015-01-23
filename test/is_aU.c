int __is_aU(void *, const char *);

int main(void) {
    int *x;
    __is_aU(x, "int32");
    return 0;
}
