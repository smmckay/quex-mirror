/* Socket-Based Lexical Analyzer
 * -----------------------------
 *
 * This application implements a lexical analyzer that directly reads content
 * from a socket connection. For trying, the socket connection may be fed
 * with the 'feeder-socket.c' application which reads content from a file
 * and passes it trough the socket.
 *
 * As soon as a "bye" lexeme is received, the application terminates.
 *
 *           socket feeder                          lexer-socket
 *          .----------------------.               .-------------------------.
 * .------. |    .--------.        |               |           .----------.  |
 * | file |-+--->| socket |    .--------.      .--------.      | lexical  |  |
 * '------' |    | feeder |--->| socket |----->| socket |----->| analyzer |  |
 *          |    '--------'    '--------'      '--------'      '----------'  |
 *          '----------------------'               '-------------------------'
 *
 *
 * (C) Frank-Rene Schaefer
 *                                                                           */
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>

#include <LexAscii.h>

static int  setup_socket_server(void);
static bool accept_and_lex(int listen_fd);
static void print_token(quex_Token*  token);
 
int main(void)
{
    int listen_fd = setup_socket_server();

    if( listen_fd == - 1) return -1;

    while( accept_and_lex(listen_fd) );

    return 0;
}

static bool
accept_and_lex(int listen_fd)
/* Accept an incoming connection and let a lexical analyser be fed by what 
 * comes through it.
 *
 * RETURNS: True, lexing successful.
 *          False, if an error occured or the 'BYE' token requests to stop.  */
{
    int            connected_fd = accept(listen_fd, (struct sockaddr*)NULL ,NULL); 
    quex_Token*    token;
    quex_LexAscii  qlex;
    ByteLoader*    loader = ByteLoader_POSIX_new(connected_fd);

    if( connected_fd == -1 ) {
        printf("server: accept() terminates with failure.\n");
        sleep(1);
        return true;
    }

    /* A handler for the case that nothing is received over the line. */
    loader->on_nothing = self_on_nothing;

    QUEX_NAME(from_ByteLoader)(&qlex, loader, NULL);

    do {
        QUEX_NAME(receive)(&qlex, &token);

        print_token(token);

        if( token->_id == QUEX_TKN_BYE ) return false;

    } while( token->_id != QUEX_TKN_TERMINATION );
        
    QUEX_NAME(destruct)(&qlex);

    return true;
}


static int 
setup_socket_server(void)
/* Setup a socket server, i.e. something that can listen on incoming 
 * connections. 
 *
 * RETURNS: -1, in case of failure.
 *          file descriptor of a listening socket.                           */
{
    int                 listen_fd = 0;
    struct sockaddr_in  addr;

    listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    if( listen_fd == -1 ) {
        printf("server: socket() terminates with failure.\n");
        return -1;
    }

    memset(&addr, 0, sizeof(addr));
    addr.sin_family      = AF_INET;    
    addr.sin_addr.s_addr = htonl(INADDR_ANY); 
    addr.sin_port        = htons(0x4711);    

    if( bind(listen_fd, (struct sockaddr*)&addr, sizeof(addr)) == -1 ) {
        printf("server: bind() terminates with failure.\n");
        return -1;
    }

    if( listen(listen_fd, 10) == -1 ) {
        printf("server: listen() terminates with failure.\n");
        return -1;
    }

    return listen_fd;
}

static void
print_token(quex_Token*  token)
{
    size_t PrintBufferSize = 1024;
    char   print_buffer[1024];

    printf("   Token: %s\n", QUEX_NAME_TOKEN(get_string)(token, print_buffer, 
                                                         PrintBufferSize));
}
