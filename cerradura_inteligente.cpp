#include <iostream>
#include <list>

using namespace std;

list<int> CODIGO = {8,9,4,9,1};

//funcion para validar el input
bool validacion(int input){
    bool error = false;
    int codigo = 0;

    //verificar si el input pasa la
    //la conversion hacia int
    if(cin.fail()){
        error = true; 
        codigo = 1;
    }

    if(error){
        cout<<"--- ERROR ---"<<endl;
        switch(codigo){
            case 1:
                cout<<"ingreso un valor no numerico."<<endl;
                return false;
                break;
            default:
                cout<<"Desconociodo..."<<endl;
                return false;
        } 
    }
    return true;
}

//funcion para validar si el codigo esta correcto
bool validar_codigo(list<int>& codigo_ingresado) {
    // Verificar que tengan el mismo tamaño
    if(codigo_ingresado.size() != CODIGO.size()) {
        return false;
    }
    
    // Comparar elemento por elemento usando iteradores
    auto it_ingresado = codigo_ingresado.begin();
    auto it_codigo = CODIGO.begin();
    
    //mientras el iterador no este en el final de las respectivas listas; corre.
    while(it_ingresado != codigo_ingresado.end() && it_codigo != CODIGO.end()) {
        //desreferencia los iteradores para tener el digito
        if(*it_ingresado != *it_codigo) {
            return false;
        }
        //incrementa los iteradores
        it_ingresado++;
        it_codigo++;
    }
    return true;
}

int main(){
    int iteracion = 0; //trackea porque instacia del codigo ingresado va
    int intentos = 0; //trackea la cantidad de intentos
    list<int> codigo_ingresado = {}; int digito = 0; //guarda el input del usuario
    bool input_valido = false; //verifica si cumple con los requisitos de input
    bool acceso = false; //verifica si es el codigo correcto

    cout<<"GoodLook"<<endl;
    cout<<"Ingrese un codigo:";
    //pedirle al usuario que ingrese el codigo
    while(iteracion<5){
        cin>>digito;

        //validacion de input
        input_valido = validacion(digito);
        if(!input_valido){ return -1; }

        codigo_ingresado.push_back(digito);
        iteracion += 1;
    } 

    //validar que el codigo sea correcto
    acceso = validar_codigo(codigo_ingresado);

    //do{ intentos += 1;}while(intentos<5);
    
    //ACCESO DENEGADO
    if(!acceso){
        cout<<"--- BLOQUEADO ---"<<endl;
        return 10;
    }

    //FIN DEL PROGRAMA
    cout<<"Bienvenido!"<<endl;
    return 0;
}