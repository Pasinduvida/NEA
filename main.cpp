#include <iostream>
#include <string>
using namespace std;

class Car{
private:
    string brand;
    string model;
    
public:
    Car(string b, string m){
        brand = b;
        model = m;
    }
    string getBrand(){
        return brand;
    }
    string getModel(){
        return model;
    }
    
    
};

int main(){
    Car a("BMW", "I8");
    Car b("Audi", "Q7");
    cout << a.getModel() << endl;
    cout << b.getModel() << endl;
}
