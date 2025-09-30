<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="19008000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="CalculateSinus.vi" Type="VI" URL="../CalculateSinus.vi"/>
		<Item Name="GenerateRandomNoise.vi" Type="VI" URL="../GenerateRandomNoise.vi"/>
		<Item Name="main.vi" Type="VI" URL="../main.vi"/>
		<Item Name="StateSpaceModel.vi" Type="VI" URL="../StateSpaceModel.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="CD Generic Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/CD Generic Error Handler.vi"/>
				<Item Name="CD Get 3D Time Data.vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/Plots.llb/Plots subVIs/CD Get 3D Time Data.vi"/>
				<Item Name="CD Get All Frequency Response Data.vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/Plots.llb/CD Get All Frequency Response Data.vi"/>
				<Item Name="CD plot data.vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/Plots.llb/CD plot data.vi"/>
				<Item Name="CD Set 3D Time Data.vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/Plots.llb/Plots subVIs/CD Set 3D Time Data.vi"/>
				<Item Name="cd_Add Nyquist Arrow.vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/Plots.llb/Plots subVIs/cd_Add Nyquist Arrow.vi"/>
				<Item Name="cd_Bode (LinSys State-Space).vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Frequency Response Analysis/Frequency Response.llb/Frequency Response subVI/cd_Bode (LinSys State-Space).vi"/>
				<Item Name="cd_Check Plots IO (State-Space).vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/Plots.llb/Plots subVIs/cd_Check Plots IO (State-Space).vi"/>
				<Item Name="cd_Check Plots IO (Transfer Function).vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/Plots.llb/Plots subVIs/cd_Check Plots IO (Transfer Function).vi"/>
				<Item Name="cd_Check Plots IO (ZPK).vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/Plots.llb/Plots subVIs/cd_Check Plots IO (ZPK).vi"/>
				<Item Name="cd_Check Plots IO.vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/Plots.llb/Plots subVIs/cd_Check Plots IO.vi"/>
				<Item Name="cd_Create Nyquist Arrows.vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/Plots.llb/Plots subVIs/cd_Create Nyquist Arrows.vi"/>
				<Item Name="cd_Plot Frequency Response (TF).vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/Plots.llb/Plots subVIs/cd_Plot Frequency Response (TF).vi"/>
				<Item Name="cd_Plot Frequency Response.vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/Plots.llb/Plots subVIs/cd_Plot Frequency Response.vi"/>
				<Item Name="cd_Plot Margin Lines (TF).vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/Plots.llb/Plots subVIs/cd_Plot Margin Lines (TF).vi"/>
				<Item Name="cd_Plot Margin Lines.vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/Plots.llb/Plots subVIs/cd_Plot Margin Lines.vi"/>
				<Item Name="cd_Plot Outputs Or States.vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/Plots.llb/Plots subVIs/cd_Plot Outputs Or States.vi"/>
				<Item Name="cd_Set Graph Display Props.vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/Plots.llb/Plots subVIs/cd_Set Graph Display Props.vi"/>
				<Item Name="cd_Set Plot Names.vi" Type="VI" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/Plots.llb/Plots subVIs/cd_Set Plot Names.vi"/>
				<Item Name="NI_AALBase.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALBase.lvlib"/>
				<Item Name="NI_AALPro.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALPro.lvlib"/>
				<Item Name="NI_CD_Dynamic Analysis.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Dynamic Analysis/NI_CD_Dynamic Analysis.lvlib"/>
				<Item Name="NI_CD_Frequency Response.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Frequency Response Analysis/NI_CD_Frequency Response.lvlib"/>
				<Item Name="NI_CD_LinSys State-Space.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/NI_CD_LinSys State-Space.lvlib"/>
				<Item Name="NI_CD_Model Delay.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Model Delay/NI_CD_Model Delay.lvlib"/>
				<Item Name="NI_CD_Model Type.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Model Conversions/NI_CD_Model Type.lvlib"/>
				<Item Name="NI_CD_State-Space Analysis.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_State-Space Analysis/NI_CD_State-Space Analysis.lvlib"/>
				<Item Name="NI_Gmath.lvlib" Type="Library" URL="/&lt;vilib&gt;/gmath/NI_Gmath.lvlib"/>
				<Item Name="NI_LinSys_Data Typedefs.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Model Construction/NI_LinSys_Data Typedefs.lvlib"/>
				<Item Name="NI_LinSys_LinSys Conversion.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/NI_LinSys_LinSys Conversion.lvlib"/>
				<Item Name="NI_LinSys_LinSys Delay.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/NI_LinSys_LinSys Delay.lvlib"/>
				<Item Name="NI_LinSys_LinSys State-Space Shared.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/NI_LinSys_LinSys State-Space Shared.lvlib"/>
				<Item Name="NI_LinSys_LinSys TF.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/NI_LinSys_LinSys TF.lvlib"/>
				<Item Name="NI_LinSys_LinSys ZPK.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/NI_LinSys_LinSys ZPK.lvlib"/>
				<Item Name="NI_LinSys_Matrix AAL.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/NI_LinSys_Matrix AAL.lvlib"/>
				<Item Name="NI_LinSys_Matrix Math.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/NI_LinSys_Matrix Math.lvlib"/>
				<Item Name="NI_LinSys_Model Creation.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Model Construction/NI_LinSys_Model Creation.lvlib"/>
				<Item Name="NI_LinSys_Model Information.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Model Construction/NI_LinSys_Model Information.lvlib"/>
				<Item Name="NI_LinSys_Model Typedefs.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Model Construction/NI_LinSys_Model Typedefs.lvlib"/>
				<Item Name="NI_LinSys_Polynomial Math.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/NI_LinSys_Polynomial Math.lvlib"/>
				<Item Name="NI_LinSys_String Utilities.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/Control Design/_Utility/NI_LinSys_String Utilities.lvlib"/>
				<Item Name="NI_Matrix.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/Matrix/NI_Matrix.lvlib"/>
			</Item>
			<Item Name="lvanlys.dll" Type="Document" URL="/&lt;resource&gt;/lvanlys.dll"/>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
