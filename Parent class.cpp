#include <iostream>
#include <string>
using namespace std;

class Teacher{
private:
    string name;
    string subject;
    string room;
public:
    string getname(string name = "Pasindu"){
        return name;
    }
    string getsubject(string subject){
        return subject;
    }
    string getroom(string room){
        return room;
    }
};

int main(){
    Teacher obj;
    cout << obj.getname() << endl;
    
}
