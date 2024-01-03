#include <iostream>

using namespace std;

class MyClass {
  public:
    MyClass() {};

    void print_from_class() {
      cout << "printed from class" << endl;
    };
};

void print_sentence() {
  cout << "printing sentence from function" << endl;
}

int main () {
  cout << "simple target cpp file!" << endl;
  print_sentence();

  MyClass test_class = MyClass();
  test_class.print_from_class();

  return 0;
}
