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
    string getsubject(){
        return subject;
    }
    string getroom(){
        return room;
    }
};

int main(){
    Teacher obj1("Pasindu", "Maths","IT");
    Teacher obj2("Janith", "Science", "MA3");
    cout << obj1.getname() << endl;
    cout << obj2.getsubject() << endl;
    
    
}
