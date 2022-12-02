import utils.py

def make_class(line):
    """
    IN/OUT => NUMBER of bool inputs/outputs
    FORMULAS => separated by " | "
    nodes in formulas should be written like this : NAME[id]-[output id] (NOT1-1) par exemple 
    (output id starts at 1)
    """
    NAME, IN, OUT, FORMULAS = line.split(maxsplit=3)
    IN, OUT = int(IN), int(OUT)
    constructor_args = ", ".join([f"bool * IN{i+1} = &OFF" for i in range(IN)])
    INptr_init = f"{{{','.join([f'IN{i+1}' for i in range(IN)])}}}"
    make_intern = 
    # components = sorted(list(set(map(lambda x: x.split("-")[0], FORMULAS.replace("("," ").replace(")"," ").replace(","," ").split(" ")))))
    #for i in range(len(rq_intr)):
    #    FORMULAS=FORMULAS.replace(rq_intr[i], f"intern[i]->OUTval[0]")
    # FORMULAS = FORMULAS.split(" | ")
    baked = f"""
    
    class {NAME} : public component {{
    public:
        bool * INptr[{IN}], INval[{IN}], OUTval[{OUT}] = {{&OFF}};
        int IN, OUT;
        node_ptr_vector intern;
        void getInputs() {{
            for(int i = 0; i < IN; i++){{
                INval[i] = *(INptr[i]);
            }}

            intern.getInputs();
        }};
        
        void getOutputs() {{
            OUTval[0] = !(INval[0]);
            intern.getOutputs();
        }};

        void quickCompute() {{
            getInputs(); 
            getOutputs();
        }}
        
        {NAME}({constructor_args}):INptr{INptr_init}, IN({IN}), OUT({OUT}) {{
            
        }};

        std::string repr() {{
            std::string result = "{NAME} =>\t";
            if(OUT == 0) {{return result + "no output";}}
            result += "OUT1 : " + std::to_string(OUTval[0]);
            for (int i = 1; i < OUT; i++) {{
                result += " | OUT" + std::to_string(i+1) + " : " + std::to_string(OUTval[i]);
            }}
            return result;
        }}
    }};"""

    return baked

header = r"""#include <iostream>
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
    };"""

footer = """
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
}"""

body = [
    "NOT 1 1 NAND(IN1)",
]

body = map(make_class, body)
body = "\n".join(body)

with open("main.cpp", "w") as f:
    f.write(header)
    f.write(body)
    f.write(footer)

import os
os.system("g++ main.cpp -o main")
os.system(f".{os.sep}main")