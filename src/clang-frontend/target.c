#include <stdio.h>

void print_number(int x, int y, int z){
  printf("print %d%d%dnumber from function\n", x, y, z);
}

int main() {
  printf("printing from main\n");
  print_number(9, 2, 6);
  return 0;
}
