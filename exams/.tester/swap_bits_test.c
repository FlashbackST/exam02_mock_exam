#include <stdio.h>

unsigned char	swap_bits(unsigned char octet);

static int	failed = 0;

static void	check(unsigned char got, unsigned char expected, const char *name)
{
	if (got != expected)
	{
		printf("FAIL [%s]: got %d, expected %d\n", name, got, expected);
		failed++;
	}
}

int	main(void)
{
	/* swap_bits swaps the 4 high bits with the 4 low bits */
	check(swap_bits(0), 0, "0");
	check(swap_bits(255), 255, "255");
	check(swap_bits(0x0F), 0xF0, "0x0F->0xF0");
	check(swap_bits(0xF0), 0x0F, "0xF0->0x0F");
	check(swap_bits(0x12), 0x21, "0x12->0x21");
	check(swap_bits(0xAB), 0xBA, "0xAB->0xBA");
	check(swap_bits(0x01), 0x10, "0x01->0x10");
	check(swap_bits(0x10), 0x01, "0x10->0x01");
	check(swap_bits(0x42), 0x24, "0x42->0x24");
	check(swap_bits(0xCD), 0xDC, "0xCD->0xDC");
	check(swap_bits(0x55), 0x55, "0x55->0x55");
	check(swap_bits(0xAA), 0xAA, "0xAA->0xAA");
	if (!failed)
		printf("ALL TESTS PASSED\n");
	return (failed > 0);
}
