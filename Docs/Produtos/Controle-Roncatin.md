**.github**
	workflows
		dotnet-maui-buil.yml
			name: .NET MAUI Build & Deploy
		on:
		  push:
		    branches: [ "master" ]
		  pull_request:
		    branches: [ "master" ]
		  workflow_dispatch:
		
		jobs:
		  build-android:
		    name: Build Android
		    runs-on: windows-latest
		    
		    steps:
		    - name: Checkout
		      uses: actions/checkout@v4
		      with:
		        fetch-depth: 0
		
		    - name: Setup .NET 9
		      uses: actions/setup-dotnet@v4
		      with:
		        dotnet-version: '9.0.x'
		
		    - name: Install .NET MAUI workload
		      run: dotnet workload install maui
		
		    - name: Restore dependencies
		      run: dotnet restore Controle-Roncatin.csproj
		
		    - name: Build Android (Debug)
		      if: github.event_name == 'pull_request'
		 run: |
		dotnet build Controle-Roncatin.csproj `
		 -f net9.0-android `
		      -c Debug
		
		    - name: Build Android AAB (Release)
		      if: github.event_name == 'push' && github.ref == 'refs/heads/master'
		      run: |
		  dotnet publish Controle-Roncatin.csproj `
		   -f net9.0-android `
		          -c Release `
		          -p:AndroidPackageFormat=aab
		      # Nota: Para assinar o AAB, adicione as secrets:
		      # ANDROID_KEYSTORE_BASE64, KEYSTORE_PASSWORD, KEY_ALIAS, KEY_PASSWORD
		      # e descomente as linhas de assinatura no .csproj
		
		    - name: Upload Android Artifact
		      if: github.event_name == 'push' && github.ref == 'refs/heads/master'
		      uses: actions/upload-artifact@v4
		      with:
		        name: android-aab
		        path: |
		          **/*.aab
		          **/*.apk
		        retention-days: 30
		
		  build-windows:
		    name: Build Windows
		    runs-on: windows-latest
		    
		    steps:
		    - name: Checkout
		   uses: actions/checkout@v4
		      with:
		        fetch-depth: 0
		
		    - name: Setup .NET 9
		   uses: actions/setup-dotnet@v4
		      with:
		        dotnet-version: '9.0.x'
		
		    - name: Install .NET MAUI workload
		      run: dotnet workload install maui
		
		- name: Restore dependencies
		   run: dotnet restore Controle-Roncatin.csproj
		
		    - name: Build Windows (Debug)
		      if: github.event_name == 'pull_request'
		      run: |
		        dotnet build Controle-Roncatin.csproj `
		          -f net9.0-windows10.0.19041.0 `
		          -c Debug
		
		  - name: Publish Windows (Release)
		      if: github.event_name == 'push' && github.ref == 'refs/heads/master'
		      run: |
		        dotnet publish Controle-Roncatin.csproj `
		          -f net9.0-windows10.0.19041.0 `
		          -c Release `
		 -p:RuntimeIdentifierOverride=win10-x64 `
		          -o ./publish/windows
		
		    - name: Upload Windows Artifact
		      if: github.event_name == 'push' && github.ref == 'refs/heads/master'
		      uses: actions/upload-artifact@v4
		      with:
		      name: windows-exe
		        path: ./publish/windows/**/*
		   retention-days: 30
		
		  build-ios:
		    name: Build iOS
		    runs-on: macos-latest
		    
		    steps:
		    - name: Checkout
		      uses: actions/checkout@v4
		      with:
		        fetch-depth: 0
		
		    - name: Setup .NET 9
		      uses: actions/setup-dotnet@v4
		      with:
		      dotnet-version: '9.0.x'
		
		    - name: Install .NET MAUI workload
		      run: dotnet workload install maui
		
		    - name: Restore dependencies
		      run: dotnet restore Controle-Roncatin.csproj
		
		  - name: Build iOS (Debug)
		      if: github.event_name == 'pull_request'
		      run: |
		     dotnet build Controle-Roncatin.csproj \
		          -f net9.0-ios \
		          -c Debug
		
		    - name: Build iOS (Release)
		      if: github.event_name == 'push' && github.ref == 'refs/heads/master'
		   run: |
		        dotnet build Controle-Roncatin.csproj \
		          -f net9.0-ios \
		     -c Release
		      # Nota: Para assinar e publicar no App Store, voc� precisa:
		      # - Certificado de distribui��o iOS
		      # - Provisioning Profile
		      # - Adicionar secrets no GitHub
		
		    - name: Upload iOS Artifact
		      if: github.event_name == 'push' && github.ref == 'refs/heads/master'
		      uses: actions/upload-artifact@v4
		      with:
		   name: ios-app
		        path: |
		          **/*.ipa
		  **/*.app
		        retention-days: 30
		
		  build-macos:
		    name: Build macOS
		  runs-on: macos-latest
		    
		    steps:
		    - name: Checkout
		   uses: actions/checkout@v4
		      with:
		  fetch-depth: 0
		
		    - name: Setup .NET 9
		      uses: actions/setup-dotnet@v4
		      with:
		        dotnet-version: '9.0.x'
		
		    - name: Install .NET MAUI workload
		   run: dotnet workload install maui
		
		    - name: Restore dependencies
		    run: dotnet restore Controle-Roncatin.csproj
		
		    - name: Build macOS (Debug)
		      if: github.event_name == 'pull_request'
		      run: |
		        dotnet build Controle-Roncatin.csproj \
		       -f net9.0-maccatalyst \
		      -c Debug
		
		    - name: Build macOS (Release)
		      if: github.event_name == 'push' && github.ref == 'refs/heads/master'
		      run: |
		        dotnet build Controle-Roncatin.csproj \
		          -f net9.0-maccatalyst \
		   -c Release
		
		    - name: Upload macOS Artifact
		      if: github.event_name == 'push' && github.ref == 'refs/heads/master'
		      uses: actions/upload-artifact@v4
		      with:
		        name: macos-app
		        path: |
		        **/*.pkg
		    **/*.app
		        retention-days: 30
		
			copilot-instructions.md
**.vs**
		Controle-Roncatin
			config
					applicationhost.config
			copilot-chat
				6b6ab15e
					sessions
							9ca69a78-0fcf-4b55-921d-25128ce4e3ac
							86994994-b648-4580-9837-c28abf2b6a15
			CopilotIndices
				17.14.1368.60722
					CodeChunks.db
					CodeChunks.db.shm
					CodeChunks.db-wal
					SemanticSymbols.db
					SemanticSymbols.db-shm
					SemanticSymbols.db-wal
					
			DesignTimeBuild
				.dtbcache.v2
			FileContentIndex
				2ae988e0-bde0-4a2c-8fa75492bfd685c9.vsidx
				264d24c7-c47c-4fb3-8a1e-eca1ab17b6db.vsidx
				e5e6e1e1-6bdb-4e19-9849-201843ffd8c7.vsifx
				fdbfea93-90f2-4237-bc33-44babdfa5e3d.vsidx
				fea03f08-0f6a-42f8-846a-d2e63be7c159.vsidx
			
			v17
				.futdcache.v2
				.suo
				DocumentLayout.backup.json
				DocumentLayout.json
				
		
	CopilotSnapshots
	789AA69CCF0F554B921D25128CE4E3AC
		DE39907049B590498F886988AB43247D
			0A7F229A002D7D3E9011FODA5D5BD37C
			OB13311F859EB68E9C16252E6F72AB39
			OD5FOB738EC1EB4A0FE041E00698F1B3
			1C887D6CAFACB266BD99A06030C331F0
			1C4292C661C20EE009BC34BE91DA51DC
			1E503802178E9F1C0861C4CB3E76CA06
			1F14676926DB574A9959066EBD52429B
			06FOEBE1322B4923E934E970130B4708
			6EB95D283D62E322FD4F8C2FCDE66510
			8B5CE5DF592E4551977BAF5A45D9440E
			8BDF39A4599E45E8DEC82FA5F5FB98AA
			8D3FBFB20D3F5COEF82D80951FBDE573
			8FB563780998FCE2F38CF0B7E23DF6E7
			09FC59CD7D92B4E784937E8907A6829C
			9B7A29C64AE7A7369462D804AB46C418
			9E4E32C14B16C476AECE9F7D022C41CE
			9E79E38993D54D250BE8931CD8C9F34A
			15CC9538FCBE34FOD15FBB220FEEABAE
			29FF425E5B08F6378233694BD3ED9AEE
			31B8EE9309D3A77E1899919B40A5E950
			38DC122DA6C21CCBC434F4F07082BC87
			40D31EE74183668818C2A01B1729AA78
			81B70D3CE28CC93A65DAB15D2B4F9F0A
			85DF5962FDADFD46BD726D5BDB0D02D4
			95D5319540F5467809F2DC32D036F5B4
			380EABBCFF6F6E8A29F08A33BCCB161C
			655E3439704D144BAF9C095B61FFD8C7
			755D62E58485A261996E1233BE88B7D7
			942E6D76849B60E752A426AA691468DD
			5906C548352CF573C483D88144192130
			6697A7C90DBE8C06206B7A4A60391CE3
			7061F031430991E3ADFE5789119A0655
			7440A0652B0E45FCE9FC7DD2E2B104A8
			79330BA8399BC4B05F85B0AF967024CD
			1513489BBC2DAB8309E3FADDD3AD0149
			8019802E025FOF1143672747DADBD378
			363646471945266E0401D5DC52AB2B51
			A1B59A2B829617B3901205A0DE3C0936
			AC32819550D04209BCCEE301A59E4F80
			AEBEC9786E7FD49C221C0872CED69EOF
			B4D6C40DCE8207426854DE4FF5218064
			B67907481DA4BF4579863AE6796D500B
			B2007849662FBBADA8DE99B5EAEAAA49
			BE021DOC40148C5B80ECBA64C8140D91
			C6D2414C136B375755DA6DA7B60CB4F4
			D049C732CC6606C19C7E931571258BC1
			DF3460EC82611FFA7844176FC94A8CA0
			E3DEEA1F5F18428A883877AA2C9A4DBA
			E24BDEB0823BE8B1D63A3AE449487786
			E56D433DA236355DB6B5EDEA3A94F40A
			E576CE71C60E8097C827C1505474595F
			EDF803A528FBDCB40498BADC8DFFA225
			EEFDD05DDD187303F674C6B9F9CD37D0
			F1CB175C8C38C5C447CA58AE7A21FFE4
			F9D259714C13B67E2E4C9EB4B4373675
			FB7F6639A4E5CD42C81DE5693BF6B1B9
			FFCF7A08484EB1BEOBB316C30A2A669C				
		FEC3832E6D66CD42AC1EC2323232EE54
			1C887D6CAFACB266BD99A06030C331F0
			1F1F069DF7216DE33EA079C34E3F6D4B
			03D932E69E7E5CD692A10F2E8C5C197A
			3ACFADE38F5B2F63A23267D1EA3F82F6
			4C5D6292CD726DAC50C61F2D966DDBD8
			4D5E8F8FE2CFF13D116E4096A2B49D7E
			5F0726BA801E1CC8000F78FE69230610
			7B3A83E75ABF75C9C16AA81AA10EAF36
			7E2D7E7BAE1230510745E2E25AD7A147
			7F0B8348E1E848DDEA8507487DAA11F5
			8B1F179C6F65B5DAE2B6C7E62FF0F21B
			9CD4EAA97EC40C552AF3982786976705
			28C970BA911744AFC86E27BD72816835
			36E76AFD0D71BB3D40EC22E05C783D06
			38ACB333C572B452200A338388ABD9BA
			54EA4DEA963CB84F8533C1AD4A0D5511
			61E310BAC920E7E0ED5409006C787866
			79CF4A22EB95DD165740163F2DD7C3B2
			96D91D930B6863B3E2D82D7C4B46EDB4
			179F39CABE70BA71F3B280AE2BD71AD2
			370E276647A3499B842068AF186F7AA1
			718A18B11352ACDAC90BFB47F68859C3
			751D0334570DD70464E9D25B8303A8E0
			942E6D76849B60E752A426AA691468DD
			2594B31DBD49C252076190593D3318A6
			4678CDA004CA1EF9AA648BEF9E33E559
			05444B1F716FD976A8F8392BA627D1FD
			5906C548352CF573C483D88144192130
			847103063C778BCA0CDC168BA1C3A9E6
			A1CEF04DF7EA292F0F4CC9AEEDEAE5E0
			A43CFDCC3D5F1DB9A0F4CB55825DA507
			BF59FD27D3F8E20ED0BD575F0BE18C0F
			C6D2414C136B375755DA6DA7B60CB4F4
			CB3515822F6713C327F88243BB3068C8
			DF0A5E2009C0EC6965CE411D951EE8EE
			E7C3FE8015A342C00E7D4A115829F397
			ED3FA5E90624344F48EB66F06674DADA
			EF4C7685750DE960FA8DD51B7CB9C4FE
			F4C3A38E60F9EC2E60987661FAA8A30A
			F6F3A2F67D0CF9FC255AB4EA8764CECE
			F7480C9C471E61D7D5F00EA9418DF86E
		state.mpack - Corrompido
	9449998648B680459837C28ABF2B6A15
		6E4F75ADDC531C43A2766FE826598C07
			1F38C82F5FA1AF3937C043E20B8BF210
			5A3C1E5DB49075B9DC67B85FF61C16A8
			5BCCBE44605F01BFA3458697DBBDF49A
			2951CEBEAOCOEB0511B2B8DEBOE58EF6
			9015B22019586CB8AF97E1AB8AOBE03E
			3051501B52A03704D78C19DEF7FC2228
			5437579F6A58290AD09B7276428F174F
			A78D687EB257268F3F7B6285CB9A78FB
			B496178BA7BC05E21AA3E98758AB929E
			C6CDCD69B821817F4A988C51EDD48BE6
			C3682569E714E32640E443CFF8E630D1
			D2943B6CE6364CDC8278BD45B347B631
			E62CE4908C9339CD5C484C3F96219831
			E73C650F745B7991044A7AD8FD884D86
		338D43A3A4662148BCE1BD39FAD206B1
			1D4B5DED7A30AF10BAB53CDB8A16653E
			1F38C82F5FA1AF3937C043E20B8BF210
			5C369026DB1FE63E295A53B639C8C318
			5FB4C7CDCE755F59F512776E8BDD790B
			6B038BBCOB7FEAA1962B1C14AABD1CDE
			6D943880506395DA41F391B965C99695
			8B5F2D6776F846BB18E8674DF1F69C74
			9FCF5B778147D21C5436D4EDFC2A7DCA
			44FB4B3F67E8909B516A71F3801E2CEE
			60F7345DB168FFFF250D63450860A770
			918CD9D4BB2CB5B4A33E73C90FE02F1A
			5906C548352CF573C483D88144192130
			6762CFFD02D4B4DF44853A7D3D219CCD
			9015B22019586CB8AF97E1AB8AOBE03E
			3051501B52A03704D78C19DEF7FC2228
			A2838CEDF9BF363BB428065063C6970C
			ACD43B84F47FE54A4DF0DEF53DC55C74
			BOD547FF63671457EC34C404A9C27D1A
			B8AD1579D0B77B4B3DCDEDE6002E5D69
			B114B0691F64266473F38E2B8233456B
			B702F8EE0584C600608BE70D019866C4
			B719AF3665F169B845FFB61D33E9B98D
			BA128DC8FFFC3FBF4BB6551E048868F2
			C4B8F784117418DD406A211F84B16D02
			C6CDCD69B821817F4A988C51EDD48BE6
			8BEDB6E434842E10E127A185EEE9511
			C3682569E714E32640E443CFF8E630D1
			D5EA6243BCEEE43459C4107FC8DBB045
			D58C3C7B80D3EAFF1262DBC68371A20A
			E62CE4908C9339CD5C484C3F96219831
			F057781B6846EFB621F96D18BB5EF429
			FBE23B16C4293407906A64FA4B22924F
			FFCF7A08484EB1BE0BB316C30A2A669C
		state
	ProjectEvaluation
		controle-roncatin.metadata.v9.bin
		controle-roncatin.projects.v9.bin
		controle-roncatin.strings.v9.bin

**bin**
	Debug
		net9.0-android
			#VAZIA
		net9.0-ios
			net9.0-maccatalyst
				#VAZIA
		net9.0-windows10.0.19041.0
			win10-x64
				af-ZA
				am-ET
				ar
				ar-SA
				as-IN
				az-Latn-AZ
				bg-BG
				bn-IN
				bs-Latn-BA
				ca
				ca-ES
				ca-Es-Valencia
				Components
				Controle-Roncatin.exe.WEbView2
				cs
				cs-CZ
				cy-GB
				da
				da-DK
				de
				de-DE
				el
				el-GR
				en-GB
				en-us
				es
				es-ES
				es-MX
				et-EE
				eu-ES
				fa-IR
				fi
				fi-FI
				fil-PH
				fr
				fr-CA
				fr-FR
				ga-IE
				gd-gb
				gl-ES
				gu-IN
				he
				he-IL
				hi
				hi-IN
				hr
				hr-HR
				hu
				hu-HU
				hy-AM
				id
				id-ID
				is-IS
				it
				it-IT
				ja
				ja-jp
				ka-GE
				kk-KZ
				km-KH
				kn-IN
				ko
				kok-in
				ko-KR
				lb-LU
				Io-LA
				Lt-LT
				lv-LV
				Microsoft.UI.Xaml
				mi-NZ
				mk-MK
				ml-IN
				mr-IN
				ms
				ms-MY
				mt-MT
				nb
				nb-NO
				ne-NP
				nl
				nl-NL
				nn-NO
				NpuDetect
				or-IN
				pa-IN
				pl
				Platforms
				pl-PL
				quz-PE
				ro
				ro-RO
				ru
				ru-RU
				sk
				sk-SK
				sl-SI
				sq-AL
				sr-Cyrl-BA
				sr-Cyrl-RS
				sr-Latn-RS
				sv
				sv-SE
				ta-IN
				te-IN
				th
				th-TH
				tr
				tr-TR
				tt-RU
				ug-CN
				uk
				uk-UA
				ur-PK
				uz-Latn-UZ
				vi
				vi-VN
				wwwroot
				zh-CN
				zh-Hans
				zh-Hant
				zh-HK
				zh-TW
				AboutAssets.txt
				appicon.ico
				appiconLargeTile.scale-100.png
				appiconLargeTile.scale-125.png
				appiconLargeTile.scale-150.png
				appiconLargeTile.scale-200.png
				appiconLargeTile.scale-400.png
				appiconLogo.altform-lightunplated_targetsize-16.png
				appiconLogo.altform-lightunplated_targetsize-24.png
				appiconLogo.altform-lightunplated_targetsize-32.png
				appiconLogo.altform-lightunplated_targetsize-48.png
				appiconLogo.altform-lightunplated_targetsize-256.png
				appiconLogo.altform-unplated_targetsize-16.png
				appiconLogo.altform-unplated_targetsize-24.png
				appiconLogo.altform-unplated_targetsize-32
				appiconLogo.altform-unplated_targetsize-48.png
				appiconLogo.altform-unplated_targetsize-256.png
				appiconLogo.scale-100
				appiconLogo.scale-125.png
				appiconLogo.scale-150.png
				appiconLogo.scale-200.png
				appiconLogo.scale-400.png
				appiconLogo.targetsize-16
				appiconLogo.targetsize-24.png
				appiconLogo.targetsize-32
				appiconLogo.targetsize-48
				appiconLogo.targetsize-256
				appiconMediumTile.scale-100
				appiconMediumTile.scale-125
				appiconMediumTile.scale-150
				appiconMediumTile.scale-200
				appiconMediumTile.scale-400
				appiconSmallTile.scale-100.png
				appiconSmallTile.scale-125.png
				appiconSmallTile.scale-150.png
				appiconSmallTile.scale-200.png
				appiconSmallTile.scale-400.png
				appiconSmallTile.scale-100.png
				appiconSmallTile.scale-125.png
				appiconSmallTile.scale-150.png
				appiconSmallTile.scale-200.png
				appiconSmallTile.scale-400.png
				appiconStoreLogo.scale-100.png
				appiconStoreLogo.scale-125.png
				appiconStoreLogo.scale-150.png
				appiconStoreLogo.scale-200.png
				appiconStoreLogo.scale-400.png
				appiconWideTile.scale-100.png
				appiconWideTile.scale-125.png
				appiconWideTile.scale-150.png
				appiconWideTile.scale-200.png
				appiconWideTile.scale-400.png
				Controle-Roncatin.deps.json
				Controle-Roncatin.dll
				Controle-Roncatin.exe
				Controle-Roncatin.pdb
				Controle-Roncatin.runtimeconfig.json
				Controle-Roncatin.staticwebassets.endpoints.json
				CoreMessagingXP.dll
				dcompi.dll
				dotnet_bot.scale-100.png
				dotnet_bot.scale-125.png
				dotnet_bot.scale-150.png
				dotnet_bot.scale-200.png
				dotnet_bot.scale-400.png
				dwmcorei.dll
				DwmScenel.dll
				DWriteCore.dll
				e_sqlite3.dll
				marshal.dll
				Microsoft.AspNetCore.Authorization.dlI
				Microsoft.AspNetCore.Components.dll
				Microsoft.AspNetCore.Components.Forms.dll
				Microsoft.AspNetCore.Components.Web.dll
				Microsoft.AspNetCore.Components.WebView.dll
				Microsoft.AspNetCore.Components.WebView.Maui.dll
				Microsoft.AspNetCore.Metadata.dll
				Microsoft.DirectManipulation.dll
				Microsoft.Extensions.Configuration.Abstractions.dll
				Microsoft.Extensions.Configuration.Binder.dll
				Microsoft.Extensions.Configuration.dll
				Microsoft.Extensions.Configuration.FileExtensions.dll
				Microsoft.Extensions.Configuration.Json.dll
				Microsoft.Extensions.DependencyInjection.Abstractions.dll
				Microsoft.Extensions.DependencyInjection.dll
				Microsoft.Extensions.FileProviders.Abstractions.dll
				Microsoft.Extensions.FileProviders.Composite.dll
				Microsoft.Extensions.FileProviders.Embedded.dll
				Microsoft.Extensions.FileProviders.Physical.dll
				Microsoft.Extensions.FileSystemGlobbing.dll
				Microsoft.Extensions.Logging.Abstractions.dll
				Microsoft.Extensions.Logging.Debug.dll
				Microsoft.Extensions.Logging.dll
				Microsoft.Extensions.Options.dll
				Microsoft.Extensions.Primitives.dll
				Microsoft.Foundation.winmd
				Microsoft.Graphics.Canvas.Interop.dll
				Microsoft.Graphics.Display.dll
				Microsoft.Graphics.Imaging.dll
				Microsoft.Graphics.Imaging.Projection.dll
				Microsoft.Graphics.Imaging.winmd
				Microsoft.Graphics.ImagingInternal.winmd
				Microsoft.Graphics.Internal.Imaging.winmd
				Microsoft.Graphics.winmd
				Microsoft.InputStateManager.dll
				Microsoft.InteractiveExperiences.Projection.dll
				Microsoft.Internal.FrameworkUdk.dll
				Microsoft.IO.RecyclableMemoryStream.dll
				Microsoft.JSInterop.dll
				Microsoft.Maui.Controls.dll
				Microsoft.Maui.Controls.Xaml.dll
				Microsoft.Maui.dll
				Microsoft.Maui.Essentials.dll
				Microsoft.Maui.Graphics.dll
				Microsoft.Maui.Graphics.Win2D.WinUI.Desktop.dll
				Microsoft.Security.Authentication.OAuth.Projection.dll
				Microsoft.Security.Authentication.OAuth.winmd
				Microsoft.UI.Composition.OSSupport.dll
				Microsoft.UI.dll
				Microsoft.UI.Input.dll
				Microsoft.UI.pri
				Microsoft.UI.Text.winmd
				Microsoft.UI.Windowing.Core.dll
				Microsoft.UI.Windowing.dll
				Microsoft.UI.winmd
				Microsoft.UI.Xaml.Controls.dll
				Microsoft.UI.Xaml.Controls.pri
				Microsoft.ui.xaml.dll
				Microsoft.UI.Xaml.Internal.dll
				Microsoft.UI.Xaml.Phone.dll
				Microsoft.ui.xaml.resources.19h1.dll
				Microsoft.ui.xaml.resources.common.dll
				Microsoft.UI.Xaml.winmd
				Microsoft.Web.WebView2.Core.dll
				Microsoft.Web.WebView2.Core.Projection.dll
				Microsoft.Windows.AI.ContentModerationInternal.winmd
				Microsoft.Windows.AI.ContentSafety.dll
				Microsoft.Windows.AI.ContentSafety.Projection.dll
				Microsoft.Windows.AI.ContentSafety.winmd
				Microsoft.Windows.AI.Foundation.winmd
				Microsoft.Windows.AI.FoundationInternal.winmd
				Microsoft.Windows.AI.GenerativeInternal.winmd
				Microsoft.Windows.AI.Imaging.dll
				Microsoft.Windows.AI.Imaging.Projection.dll
				Microsoft.Windows.AI.Imaging.winmd
				Microsoft.Windows.AI.Projection.dll
				Microsoft.Windows.AI.Text.dll
				Microsoft.Windows.AI.Text.Projection.dll
				Microsoft.Windows.AI.Text.winmd
				Microsoft.Windows.AI.winmd
				Microsoft.Windows.ApplicationModel.Background.Projection.dll
				Microsoft.Windows.ApplicationModel.Background.UniversalBGTask.dll
				Microsoft.Windows.ApplicationModel.Background.UniversalBGTask.winmd
				Microsoft.Windows.ApplicationModel.Background.winmd
				Microsoft.Windows.ApplicationModel.DynamicDependency.Projection.dll
				Microsoft.Windows.ApplicationModel.DynamicDependency.winmd
				Microsoft.Windows.ApplicationModel.Resources.dll
				Microsoft.Windows.ApplicationModel.Resources.Projection.dll
				Microsoft.Windows.ApplicationModel.Resources.winmd
				Microsoft.Windows.ApplicationModel.WindowsAppRuntime.Projection.dll
				Microsoft.Windows.ApplicationModel.WindowsAppRuntime.winmd
				Microsoft.Windows.AppLifecycle.Projection.dll
				Microsoft.Windows.AppLifecycle.winmd
				Microsoft.Windows.AppNotifications.Builder.Projection.dll
				Microsoft.Windows.AppNotifications.Builder.winmd
				Microsoft.Windows.AppNotifications.Projection.dll
				Microsoft.Windows.AppNotifications.winmd
				Microsoft.Windows.BadgeNotifications.Projection.dll
				Microsoft.Windows.BadgeNotifications.winmd
				Microsoft.Windows.Globalization.winmd
				Microsoft.Windows.Internal.Vision.winmd
				Microsoft.Windows.Management.Deployment.Projection.dll
				Microsoft.Windows.Management.Deployment.winmd
				Microsoft.Windows.Media.Capture.Projection.dll
				Microsoft.Windows.Media.Capture.winmd
				Microsoft.Windows.Private.Workloads.SessionManager.winmd
				Microsoft.Windows.PrivateCommon.winmd
				Microsoft.Windows.PushNotifications.Projection.dll
				Microsoft.Windows.PushNotifications.winmd
				Microsoft.Windows.SDK.NET.dll
				Microsoft.Windows.Security.AccessControl.Projection.dll
				Microsoft.Windows.Security.AccessControl.winmd
				Microsoft.Windows.SemanticSearch.winmd
				Microsoft.Windows.Storage.Projection.dll
				Microsoft.Windows.Storage.winmd
				Microsoft.Windows.System.Power.Projection.dll
				Microsoft.Windows.System.Power.winmd
				Microsoft.Windows.System.Projection.dll
				Microsoft.Windows.System.winmd
				Microsoft.Windows.Vision.winmd
				Microsoft.Windows.VisionInternal.winmd
				Microsoft.Windows.Widgets.dll
				Microsoft.Windows.Widgets.Projection.dll
				Microsoft.Windows.Widgets.winmd
				Microsoft.Windows.Workloads.dll
				Microsoft.Windows.Workloads.Resources.dll
				Microsoft.Windows.Workloads.Resources_ec.dll
				Microsoft.Windows.Workloads.winmd
				Microsoft.WindowsAppRuntime.Bootstrap.dll
				Microsoft.WindowsAppRuntime.Bootstrap.Net.dll
				Microsoft.WindowsAppRuntime.dll
				Microsoft.WindowsAppRuntime.Insights.Resource.dll
				Microsoft.WinUI.dll
				MRM.dll
				OpenSans-Regular.ttf
				PushNotificationsLongRunningTask.ProxyStub.dll
				resources.pri
				RestartAgent.exe
				SessionHandleIPCProxyStub.dll
				splashSplashScreen.scale-100.png
				splashSplashScreen.scale-125.png
				splashSplashScreen.scale-150.png
				splashSplashScreen.scale-200.png
				splashSplashScreen.scale-400.png
				SQLite-net.dll
				SQLitePCLRaw.batteries_v2.dll
				SQLitePCLRaw.core.dll
				SQLitePCLRaw.provider.e_sqlite3.dll
				WebView2Loader.dl
				WindowsAppRuntime.DeploymentExtensions.OneCore.dll
				WindowsAppRuntime.png
				WindowsAppSdk.AppxDeploymentExtensions.Desktop.dll
				WindowsAppSdk.AppxDeploymentExtensions.Desktop-EventLog-Instrumentation.dll
				WinRT.Runtime.dll
				WinUIEdit.dll
				workloads.365.json
				workloads.json
				workloads.lnl.json
				workloads.qnn.json
				workloads.stx.json
			
Components

Models
obj
Platforms
Properties
Resources
Services
wwwroot
App.xaml
App.xaml.cs
build-realease.ps1
Controle-Roncatin.csproj
Controle-Roncatin.csproj.user
Controle-Roncatin.sln
Deploy.md
MainPage.xaml
MainPage.xaml.cs
MauiProgram.cs



