#####
##### use this script to make add.txt look better
##### by letter
##### 2011-12-23 Empty office @ Stockholm
#####

use Data::Dumper;
use Scalar::Util qw(looks_like_number);

sub trim($) {
	my $string = shift;
	$string =~ s/^\s+//;
	$string =~ s/\s+$//;
	return $string;
}

sub handle_line {    #handle a line "Survivor	S: 23 - Ep: 15"
	my ($line) = @_;
	if ( $line =~ /(.*)(S:.*)/ ) {
		my $showname  = trim($1);
		my $episeason = trim($2);
		return ( $showname, $episeason );
	}
}

sub handle_array {
	my @array   = @_;
	my $max_len = 0;
	foreach my $element (@array) {
		if ( length( @$element[0] ) > $max_len ) {
			$max_len = length( @$element[0] );
		}
	}
	return $max_len;
}

sub handle {
	open( my $add_handle, "add.txt" ) or die "Could not open file";
	open( my $out_handle, ">add_modified.txt" )
	  or die "Could not create new file";
	my @array;
	my $pre_number = "";
	while (<$add_handle>) {
		my $line = $_;
		if ( looks_like_number($line)) {
			my $max_len = handle_array(@array);
			if ( $max_len > 0 ) {			
				print $out_handle "$pre_number";
				foreach my $element (@array) {
					printf $out_handle "%-$max_len\s\t",@$element[0];
					printf $out_handle "@$element[1]\n";
				}
				print $out_handle "\n";
				@array=();
				print "line: $line\n";
				
			}
			$pre_number = $line;
		}
		else {
			my @tmp = handle_line($line);
			push( @array, \@tmp );
		}
	}
	close($add_handle) or die "Could not close file";
	close($out_handle) or die "Could not close file";
}

handle();
