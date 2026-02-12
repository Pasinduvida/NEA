#include <iostream>
#include <string>
#include <vector>
using namespace std;

class Teacher{
private:
    string name;
    string subject;
    string room;

public:
    Teacher(string n, string s, string r){
        name = n;
        subject = s;
        room = r;
        
        
    }
    string getname(){
        return name;
    }
};

int main(){
    Teacher obj1("Pasindu","Maths","MA3");
    Teacher obj2("Janith","Science","SC3");
    Teacher obj3("Nethil", "Architecture", "AT5");
    vector<string> cars;
    cars.push_back(obj1.getname());
    cars.push_back(obj2.getname());
    cars.push_back(obj3.getname());
    
    for (int i = 0; i < cars.size(); i++){
        cout << cars[i] << endl;
    }
}
