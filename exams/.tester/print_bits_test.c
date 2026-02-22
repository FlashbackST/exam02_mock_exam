#include <stdio.h>
#include <string.h>
#include <unistd.h>

void	print_bits(unsigned char octet);

static int	failed = 0;

static void	check(unsigned char n, const char *expected, const char *name)
{
	char	buf[9];
	int		pipefd[2];
	int		bytes;

	if (pipe(pipefd) < 0)
		return ;
	int saved = dup(1);
	dup2(pipefd[1], 1);
	print_bits(n);
	fflush(stdout);
	dup2(saved, 1);
	close(saved);
	close(pipefd[1]);
	bytes = read(pipefd[0], buf, 8);
	close(pipefd[0]);
	buf[bytes] = '\0';
	if (strcmp(buf, expected) != 0)
	{
		printf("FAIL [%s]: got \"%s\", expected \"%s\"\n", name, buf, expected);
		failed++;
	}
}

int	main(void)
{
	check(0, "00000000", "0");
	check(1, "00000001", "1");
	check(2, "00000010", "2");
	check(42, "00101010", "42");
	check(255, "11111111", "255");
	check(128, "10000000", "128");
	check(127, "01111111", "127");
	check(64, "01000000", "64");
	check(85, "01010101", "85");
	check(170, "10101010", "170");
	check(16, "00010000", "16");
	check(3, "00000011", "3");
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
