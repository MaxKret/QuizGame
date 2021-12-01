TBtoGB = lambda TB: TB*1000
TB_to_PriceperGB = lambda price,TB: price/TBtoGB(TB)
n_fract_digits = lambda n: len(repr(n).split('.')[1])
# print_PriceperGB = lambda price,TB: ( "${:,.2f}".format(out := TB_to_PriceperGB(price, TB)), "${:,.3f}".format(out) )[out > 0.01]
print_PriceperGB = lambda price,TB: str("${0:,."+"{1}"+"f}").format(out := TB_to_PriceperGB(price, TB), n_fract_digits(out)+1)
for price,TB in [(49.99,1), (66.99,2), (83.72,3), (99.99,4), (240.00, 6), (307.34, 8)]:
	print(print_PriceperGB(price, TB))