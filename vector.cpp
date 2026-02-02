#include <iostream>
#include <vector>
#include <string>
using namespace std;

void num1(vector <int> x){
    for(int i = 0; i<4 ; i++){
        cout << x[i] << endl;
    }
}

int main(){
    vector<int> nums = {8, 6, 4, 9};
    num1(nums);

}

