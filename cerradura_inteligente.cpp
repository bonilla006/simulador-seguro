#include <iostream>
using namespace std;

const int CODIGO = 89491;

//funcion para validar el input
bool validacion(input){
    
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

    int codigo_ingresado = 0;
    bool acceso = false;

    do{
        cout<<"Ingrese un codigo:";
        cin>>codigo_ingresado;

        input_valido = validacion(codigo_ingresado);
        if(!input_valido){ return -1 }

        acceso = validar_codigo(codigo_ingresado);
    }while(!acceso);
    

    return 0;
}