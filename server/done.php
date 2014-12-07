<!doctype html>
<html>
<head>
	<style type="text/css">
		body {
			text-align: center;
		}
		#code {
			width: 50%;
			background: #ddd;
			border: 1px solid #ddd;
			border-radius: 5px;
			margin: auto;
			text-align: left;
			resize: none;
		}
		#code:focus {
			outline: none;
		}
	</style>
</head>
<body>
	<h3>Thanks for registering! Copy the code below into the app window:</h3>
	<textarea id="code" rows="5"><?php echo $params['Result']; ?></textarea>
	<script type="application/javascript">
		var code = document.getElementById ("code");

		var selectCode = function() {
			code.focus();
			code.select();
		};

		code.onclick = function() {
			selectCode();
		};

		selectCode();
	</script>
</body>
</html>
