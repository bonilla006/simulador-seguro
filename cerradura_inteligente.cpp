/*
referencias:
*/
#include <iostream>
using namespace std;

const int CODIGO = 89491;

//funcion para validar el input
bool validacion(int input){
    bool error = false;
    int codigo = 0;

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
bool validar_codigo(int codigo_ingresado){
    bool validado = false;
    
    if (codigo_ingresado == CODIGO){
        return true;
    }
    cout<<"Codigo Incorrecto!"<<endl;
    return validado;
}

int main(){
    int intentos = 0;
    int codigo_ingresado = 0;
    bool input_valido = false;
    bool acceso = false;

    do{
        cout<<"Ingrese un codigo:";
        cin>>codigo_ingresado;

        input_valido = validacion(codigo_ingresado);
        if(!input_valido){ return -1; }

        acceso = validar_codigo(codigo_ingresado);
        if(acceso){ break; }
        
        intentos += 1;
    }while(intentos<5);
    
    if(!acceso){
        cout<<"--- BLOQUEANDO... ---"<<endl;
        return 10;
    }
    cout<<"Bienvenido!"<<endl;
    return 0;
}