#include <iostream>
#include <vector>
#include <string>

namespace nodes {
    bool OFF = false, ON = true;

    /*template<class T>
    void quickCompute(T * component){
        component->getInputs();
        component->getOutputs();
    }*/

    class SWITCH{
    public:
        bool state;
        SWITCH() : state(false) {};
        void flick() {state = !state;};
    };

    class component {
    public:
        virtual void getInputs() {};
        virtual void getOutputs() {};
        virtual void quickCompute() {};
        virtual std::string repr() {};
    };

    class node_ptr_vector: public std::vector<component*>{
    public:
        using std::vector<component*>::push_back;
        using std::vector<component*>::operator[];
        using std::vector<component*>::begin;
        using std::vector<component*>::end;
        node_ptr_vector operator*(const node_ptr_vector & ) const;
        node_ptr_vector operator+(const node_ptr_vector & ) const;
        virtual ~node_ptr_vector() {for (component* i : *this) {delete i;}};
        void getInputs() {
            for(component* i : *this){
                i->getInputs();
            }
        };
        void getOutputs() {
            for(component* i : *this){
                i->getOutputs();
            }
        };
        void compute() {
            getInputs();
            getOutputs();
        };
        void print() {
            for(component* i : *this){
                std::cout << i->repr() << "\n";
            }
        }
    };

    /*class node_ptr_vector : public std::vector<component*>{
    public:
        virtual ~node_ptr_vector() {for (component* i : *this) {delete i;}};
        void getInputs() {
            for(component* i : *this){
                i->getInputs();
            }
        };
        void getOutputs() {
            for(component* i : *this){
                i->getOutputs();
            }
        };
        void quickCompute() {
            for(component* i : *this){
                i->quickCompute();
            }
        };
    };*/

    class NAND : public component {
    public:
        bool * INptr[2], INval[2], OUTval[1];
        int IN, OUT;
        void getInputs() {
            for(int i = 0; i < IN; i++){
                INval[i] = *(INptr[i]);
            }
        };
        
        void getOutputs() {
            OUTval[0] = !(INval[0] && INval[1]);
        };

        void quickCompute() {
            getInputs(); 
            getOutputs();
        }
        
        NAND(bool * IN1 = &OFF, bool * IN2 = &OFF):INptr{IN1,IN2}, IN(2), OUT(1) {};

        std::string repr() {
            std::string result = "NAND =>\t";
            result += "OUT1 : " + std::to_string(OUTval[0]);
            return result;
        }
    };
    
    class NOT : public component {
    public:
        bool * INptr[1], INval[1], OUTval[1] = {&OFF};
        int IN, OUT;
        node_ptr_vector intern;
        void getInputs() {
            for(int i = 0; i < IN; i++){
                INval[i] = *(INptr[i]);
            }

            intern.getInputs();
        };
        
        void getOutputs() {
            OUTval[0] = !(INval[0]);
            intern.getOutputs();
        };

        void quickCompute() {
            getInputs(); 
            getOutputs();
        }
        
        NOT(bool * IN1 = &OFF):INptr{IN1}, IN(1), OUT(1) {
            
        };

        std::string repr() {
            std::string result = "NOT =>	";
            if(OUT == 0) {return result + "no output";}
            result += "OUT1 : " + std::to_string(OUTval[0]);
            for (int i = 1; i < OUT; i++) {
                result += " | OUT" + std::to_string(i+1) + " : " + std::to_string(OUTval[i]);
            }
            return result;
        }
    };
};

int main() {
    nodes::SWITCH a, b;
    nodes::node_ptr_vector list;
    list.push_back(new nodes::NAND(&a.state, &b.state));
    list.push_back(new nodes::NOT(&a.state));
    list.compute();
    list.print();
    a.flick();
    list.compute();
    list.print();
    b.flick();
    list.compute();
    list.print();
    return 0;
}