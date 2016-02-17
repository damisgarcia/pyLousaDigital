#if 0
	shc Version 3.8.7, Generic Script Compiler
	Copyright (c) 1994-2009 Francisco Rosales <frosal@fi.upm.es>

	shc -f digitalclass.sh digitalclass 
#endif

static  char data [] = 
#define      text_z	23
#define      text	((&data[5]))
	"\250\261\335\363\117\060\047\377\247\042\000\134\041\016\350\376"
	"\330\351\072\002\324\337\213\137\065\045\202\261\077"
#define      inlo_z	3
#define      inlo	((&data[29]))
	"\032\266\334"
#define      xecc_z	15
#define      xecc	((&data[32]))
	"\106\356\227\023\032\122\360\014\057\352\115\232\205\220\067\251"
	"\221\111"
#define      tst2_z	19
#define      tst2	((&data[51]))
	"\001\026\365\007\242\112\361\221\216\232\132\214\343\144\305\172"
	"\306\234\167\347"
#define      chk2_z	19
#define      chk2	((&data[70]))
	"\357\245\163\232\275\201\174\260\236\053\354\034\302\076\342\217"
	"\011\277\056\112"
#define      pswd_z	256
#define      pswd	((&data[95]))
	"\246\016\171\235\100\016\071\042\330\000\023\153\021\264\153\371"
	"\063\175\360\127\315\354\321\210\135\355\240\300\334\111\164\152"
	"\152\354\045\270\372\137\333\322\137\356\076\161\243\251\152\327"
	"\047\132\056\365\106\377\175\244\354\035\144\311\147\331\063\321"
	"\305\131\212\300\270\145\223\030\124\322\211\370\173\363\317\243"
	"\116\375\231\224\375\026\070\352\064\235\263\234\166\347\156\074"
	"\101\370\374\372\136\220\022\263\142\234\254\336\220\173\202\336"
	"\171\033\163\166\062\253\141\147\111\024\003\277\374\161\374\075"
	"\151\371\067\310\211\112\173\354\346\047\312\167\243\114\125\035"
	"\147\311\224\232\164\365\001\275\011\004\175\006\166\172\103\337"
	"\163\173\250\375\305\044\351\254\113\263\043\357\000\171\014\147"
	"\102\240\002\267\226\003\165\237\007\362\245\175\155\351\135\340"
	"\144\006\335\052\052\306\326\166\171\372\145\172\163\162\342\266"
	"\023\344\155\251\347\342\111\357\325\357\155\102\330\313\043\075"
	"\321\000\147\373\307\075\162\101\067\330\273\253\112\235\141\135"
	"\201\317\007\150\262\120\130\210\077\305\312\030\220\356\125\142"
	"\356\274\136\265\372\042\117\036\025\236\136\147\157\154\277\250"
	"\055\151\072\167\122\221\213\123\171\215\253\303\176\277\154\045"
	"\315\346\303\016\010\023\055\036\262\213\205\041\370\105\311"
#define      date_z	1
#define      date	((&data[393]))
	"\173"
#define      msg2_z	19
#define      msg2	((&data[394]))
	"\013\013\313\011\110\114\335\266\363\233\012\123\222\066\342\273"
	"\271\240\232\050\124"
#define      msg1_z	42
#define      msg1	((&data[422]))
	"\322\064\276\077\132\214\046\012\164\122\373\046\202\150\075\116"
	"\035\022\141\153\144\144\356\210\320\020\365\214\163\216\150\006"
	"\237\164\310\263\355\136\272\315\176\013\016\307\055\022\362\342"
	"\072\035\233\057\060\310\115\342\124\323\004"
#define      lsto_z	1
#define      lsto	((&data[474]))
	"\201"
#define      tst1_z	22
#define      tst1	((&data[479]))
	"\020\310\147\071\335\165\325\055\013\215\054\050\365\355\260\003"
	"\001\257\027\250\223\172\210\247\200\224\035\166\357\034"
#define      chk1_z	22
#define      chk1	((&data[505]))
	"\042\060\053\050\211\234\306\173\112\336\220\221\256\152\264\202"
	"\160\057\211\221\235\362\210\176\150\257\234"
#define      shll_z	10
#define      shll	((&data[534]))
	"\314\053\050\351\303\232\245\154\172\144\046\361\260\040"
#define      rlax_z	1
#define      rlax	((&data[546]))
	"\250"
#define      opts_z	1
#define      opts	((&data[547]))
	"\275"/* End of data[] */;
#define      hide_z	4096
#define DEBUGEXEC	0	/* Define as 1 to debug execvp calls */
#define TRACEABLE	0	/* Define as 1 to enable ptrace the executable */

/* rtc.c */

#include <sys/stat.h>
#include <sys/types.h>

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

/* 'Alleged RC4' */

static unsigned char stte[256], indx, jndx, kndx;

/*
 * Reset arc4 stte. 
 */
void stte_0(void)
{
	indx = jndx = kndx = 0;
	do {
		stte[indx] = indx;
	} while (++indx);
}

/*
 * Set key. Can be used more than once. 
 */
void key(void * str, int len)
{
	unsigned char tmp, * ptr = (unsigned char *)str;
	while (len > 0) {
		do {
			tmp = stte[indx];
			kndx += tmp;
			kndx += ptr[(int)indx % len];
			stte[indx] = stte[kndx];
			stte[kndx] = tmp;
		} while (++indx);
		ptr += 256;
		len -= 256;
	}
}

/*
 * Crypt data. 
 */
void arc4(void * str, int len)
{
	unsigned char tmp, * ptr = (unsigned char *)str;
	while (len > 0) {
		indx++;
		tmp = stte[indx];
		jndx += tmp;
		stte[indx] = stte[jndx];
		stte[jndx] = tmp;
		tmp += stte[indx];
		*ptr ^= stte[tmp];
		ptr++;
		len--;
	}
}

/* End of ARC4 */

/*
 * Key with file invariants. 
 */
int key_with_file(char * file)
{
	struct stat statf[1];
	struct stat control[1];

	if (stat(file, statf) < 0)
		return -1;

	/* Turn on stable fields */
	memset(control, 0, sizeof(control));
	control->st_ino = statf->st_ino;
	control->st_dev = statf->st_dev;
	control->st_rdev = statf->st_rdev;
	control->st_uid = statf->st_uid;
	control->st_gid = statf->st_gid;
	control->st_size = statf->st_size;
	control->st_mtime = statf->st_mtime;
	control->st_ctime = statf->st_ctime;
	key(control, sizeof(control));
	return 0;
}

#if DEBUGEXEC
void debugexec(char * sh11, int argc, char ** argv)
{
	int i;
	fprintf(stderr, "shll=%s\n", sh11 ? sh11 : "<null>");
	fprintf(stderr, "argc=%d\n", argc);
	if (!argv) {
		fprintf(stderr, "argv=<null>\n");
	} else { 
		for (i = 0; i <= argc ; i++)
			fprintf(stderr, "argv[%d]=%.60s\n", i, argv[i] ? argv[i] : "<null>");
	}
}
#endif /* DEBUGEXEC */

void rmarg(char ** argv, char * arg)
{
	for (; argv && *argv && *argv != arg; argv++);
	for (; argv && *argv; argv++)
		*argv = argv[1];
}

int chkenv(int argc)
{
	char buff[512];
	unsigned long mask, m;
	int l, a, c;
	char * string;
	extern char ** environ;

	mask  = (unsigned long)&chkenv;
	mask ^= (unsigned long)getpid() * ~mask;
	sprintf(buff, "x%lx", mask);
	string = getenv(buff);
#if DEBUGEXEC
	fprintf(stderr, "getenv(%s)=%s\n", buff, string ? string : "<null>");
#endif
	l = strlen(buff);
	if (!string) {
		/* 1st */
		sprintf(&buff[l], "=%lu %d", mask, argc);
		putenv(strdup(buff));
		return 0;
	}
	c = sscanf(string, "%lu %d%c", &m, &a, buff);
	if (c == 2 && m == mask) {
		/* 3rd */
		rmarg(environ, &string[-l - 1]);
		return 1 + (argc - a);
	}
	return -1;
}

#if !defined(TRACEABLE)

#define _LINUX_SOURCE_COMPAT
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <unistd.h>

#if !defined(PTRACE_ATTACH) && defined(PT_ATTACH)
#	define PTRACE_ATTACH	PT_ATTACH
#endif
void untraceable(char * argv0)
{
	char proc[80];
	int pid, mine;

	switch(pid = fork()) {
	case  0:
		pid = getppid();
		/* For problematic SunOS ptrace */
#if defined(__FreeBSD__)
		sprintf(proc, "/proc/%d/mem", (int)pid);
#else
		sprintf(proc, "/proc/%d/as",  (int)pid);
#endif
		close(0);
		mine = !open(proc, O_RDWR|O_EXCL);
		if (!mine && errno != EBUSY)
			mine = !ptrace(PTRACE_ATTACH, pid, 0, 0);
		if (mine) {
			kill(pid, SIGCONT);
		} else {
			perror(argv0);
			kill(pid, SIGKILL);
		}
		_exit(mine);
	case -1:
		break;
	default:
		if (pid == waitpid(pid, 0, 0))
			return;
	}
	perror(argv0);
	_exit(1);
}
#endif /* !defined(TRACEABLE) */

char * xsh(int argc, char ** argv)
{
	char * scrpt;
	int ret, i, j;
	char ** varg;

	stte_0();
	 key(pswd, pswd_z);
	arc4(msg1, msg1_z);
	arc4(date, date_z);
	if (date[0] && (atoll(date)<time(NULL)))
		return msg1;
	arc4(shll, shll_z);
	arc4(inlo, inlo_z);
	arc4(xecc, xecc_z);
	arc4(lsto, lsto_z);
	arc4(tst1, tst1_z);
	 key(tst1, tst1_z);
	arc4(chk1, chk1_z);
	if ((chk1_z != tst1_z) || memcmp(tst1, chk1, tst1_z))
		return tst1;
	ret = chkenv(argc);
	arc4(msg2, msg2_z);
	if (ret < 0)
		return msg2;
	varg = (char **)calloc(argc + 10, sizeof(char *));
	if (!varg)
		return 0;
	if (ret) {
		arc4(rlax, rlax_z);
		if (!rlax[0] && key_with_file(shll))
			return shll;
		arc4(opts, opts_z);
		arc4(text, text_z);
		arc4(tst2, tst2_z);
		 key(tst2, tst2_z);
		arc4(chk2, chk2_z);
		if ((chk2_z != tst2_z) || memcmp(tst2, chk2, tst2_z))
			return tst2;
		if (text_z < hide_z) {
			/* Prepend spaces til a hide_z script size. */
			scrpt = malloc(hide_z);
			if (!scrpt)
				return 0;
			memset(scrpt, (int) ' ', hide_z);
			memcpy(&scrpt[hide_z - text_z], text, text_z);
		} else {
			scrpt = text;	/* Script text */
		}
	} else {			/* Reexecute */
		if (*xecc) {
			scrpt = malloc(512);
			if (!scrpt)
				return 0;
			sprintf(scrpt, xecc, argv[0]);
		} else {
			scrpt = argv[0];
		}
	}
	j = 0;
	varg[j++] = argv[0];		/* My own name at execution */
	if (ret && *opts)
		varg[j++] = opts;	/* Options on 1st line of code */
	if (*inlo)
		varg[j++] = inlo;	/* Option introducing inline code */
	varg[j++] = scrpt;		/* The script itself */
	if (*lsto)
		varg[j++] = lsto;	/* Option meaning last option */
	i = (ret > 1) ? ret : 0;	/* Args numbering correction */
	while (i < argc)
		varg[j++] = argv[i++];	/* Main run-time arguments */
	varg[j] = 0;			/* NULL terminated array */
#if DEBUGEXEC
	debugexec(shll, j, varg);
#endif
	execvp(shll, varg);
	return shll;
}

int main(int argc, char ** argv)
{
#if DEBUGEXEC
	debugexec("main", argc, argv);
#endif
#if !defined(TRACEABLE)
	untraceable(argv[0]);
#endif
	argv[1] = xsh(argc, argv);
	fprintf(stderr, "%s%s%s: %s\n", argv[0],
		errno ? ": " : "",
		errno ? strerror(errno) : "",
		argv[1] ? argv[1] : "<null>"
	);
	return 1;
}
