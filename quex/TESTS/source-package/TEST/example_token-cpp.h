#ifndef __TOKEN_H__
#define __TOKEN_H__

namespace Test {

    struct MyToken {

    public:
        uint32_t              id;

        int   _line_n;
        int   line_number() const              { return _line_n; }
        void  set_line_number(const int Value) { _line_n = Value; }
        int  _column_n;
        int  column_number() const              { return _column_n; }
        void set_column_number(const int Value) { _column_n = Value; }

    };

extern void MyToken_copy(MyToken* me, const MyToken* Other);
extern void MyToken_construct(MyToken* __this);
extern void MyToken_destruct(MyToken* __this);
}


#endif

 	  	 
