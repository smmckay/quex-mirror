#ifndef __TOKEN_H__
#define __TOKEN_H__

typedef struct MyToken_tag {
    uint32_t    id;

    size_t _line_n;
    size_t _column_n;
} MyToken;

extern void MyToken_copy(MyToken* me, const MyToken* Other);
extern void MyToken_construct(MyToken* __this);
extern void MyToken_destruct(MyToken* __this);
/* take_text is not specified. */
#endif

 	  	 
