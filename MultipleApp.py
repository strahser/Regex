import streamlit as st
import collections
from DashBoard.DashBoardMain_ import dashboard_main
from InputView.InputViewModel.SelectDataDBModel import SelectDataDBModel
from Session.StatementConfig import StatementConstants
from Session.UploadSessionSetting import UploadSessionSettingControl
from Upload.UploadView import UploadView
from Polygons.PolygonApp import polygon_main
from PrincipalSchems.ViewControls import SchemeMain
from InsertTerminalsPandas.AppInsertTerminals import insert_terminals_main
from AhuLayout.AppAhuLayout import MainAHU
from AhuLayout.AhuView import AhuView
from AnalyticalTables.AppAnaliticalTable import main_analytical_tabel
from DownloadToExcel.Control.DownloadControl import DownloadControl
from Upload.UploadLayout import UploadLayout
from StaticData.AppConfig import MenuChapters, StaticVariable
from IFC.Homepage import main as ifc_main


class MultipleApp:
	def __init__(self):
		self.condition_excel = self._check_db_exist()

	def create_upload_data(self):
		col = st.columns(2)
		with col[0]:
			with st.expander("__Input data show__."):
				self.upload_view = UploadView()
				self.upload_view.get_upload_layout()
				self.condition_json = self.upload_view.file_json_upload
				self.upload_layout = UploadLayout(self.upload_view)
				self.upload_layout.get_files_from_memory()


		with col[1]:
			show_session, clear_session = self.session_data()
		if show_session:
			order_state = collections.OrderedDict(sorted(st.session_state.items()))  # for test striamlit
			st.write(order_state)
		if clear_session:
			st.empty()

	@staticmethod
	def _check_db_exist():
		if st.session_state[StatementConstants.table_db][StatementConstants.all_tables_db]:
			return True

	@staticmethod
	def session_data():
		session = UploadSessionSettingControl()
		with st.sidebar:
			with st.expander("Session Load"):
				session.autoload_session()
		with st.expander("__Session Config__"):
			session.load_session_download()
			show_session = st.button("Show Session")
			clear_session = st.button("Clear Session")
		return show_session, clear_session


	def dash_board(self):
		dashboard_main(self.upload_layout)

	@staticmethod
	def ifc_dash_board():
		ifc_main()

	def polygons(self):
		if self.condition_excel and self.condition_json:
			polygon_main(self.upload_layout, key=MenuChapters.polygons)
		else:
			st.warning("no loaded file json polygons")

	def scheme(self):

		if self.condition_excel and self._check_db_exist:
			schem_main = SchemeMain(self.upload_layout, key=MenuChapters.scheme)
			schem_main.main()

	def ahu(self):
		MainAHU(self.upload_layout, key=MenuChapters.ahu)

	def terminals(self):
		if self.condition_excel and self.condition_json:
			insert_terminals_main(self.upload_layout, key=MenuChapters.terminals)
		else:
			st.warning("no loaded file json polygons")

	def analytics(self):
		if self.condition_excel:
			main_analytical_tabel(self.upload_layout)

	def download(self):
		if self.condition_excel:
			DownloadControl(self.upload_layout)
