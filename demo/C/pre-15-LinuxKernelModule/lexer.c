#include <linux/module.h>    
#include <linux/kernel.h> 
#include <linux/init.h>   

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Frank-Rene Schaefer");
MODULE_DESCRIPTION("Lexical Analysis in a Kernel Module");

static int __init lexer_initialization(void)
{
    printk(KERN_INFO "Hello Quex.\n");
    return 0;    
}

static void __exit lexer_termination(void)
{
    printk(KERN_INFO "Terminating.\n");
}

module_init(lexer_initialization);
module_exit(lexer_termination);
