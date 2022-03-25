def get_input_attrs(placeholder:str,classes:list[str]=[]) -> dict :
	classes = 'form-control ' + ' '.join(classes)

	return {
		'placeholder':placeholder,
		'class':classes
	}